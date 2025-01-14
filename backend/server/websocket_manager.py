import asyncio
import datetime
from typing import Dict, List

from fastapi import WebSocket

from backend.report_type import BasicReport
from backend.chat import ChatAgentWithMemory

from gpt_researcher.utils.enum import Tone
from multi_agents.main import run_research_task
from gpt_researcher.actions import stream_output  # Import stream_output
from gpt_researcher import GPTResearcher
import json

class WebSocketManager:
    """Manage websockets"""

    def __init__(self):
        """Initialize the WebSocketManager class."""
        self.active_connections: List[WebSocket] = []
        self.sender_tasks: Dict[WebSocket, asyncio.Task] = {}
        self.message_queues: Dict[WebSocket, asyncio.Queue] = {}
        self.chat_agent = None

    async def start_sender(self, websocket: WebSocket):
        """Start the sender task."""
        queue = self.message_queues.get(websocket)
        if not queue:
            return

        while True:
            message = await queue.get()
            if websocket in self.active_connections:
                try:
                    if message == "ping":
                        await websocket.send_text("pong")
                    else:
                        await websocket.send_text(message)
                except:
                    break
            else:
                break

    async def connect(self, websocket: WebSocket):
        """Connect a websocket."""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.message_queues[websocket] = asyncio.Queue()
        self.sender_tasks[websocket] = asyncio.create_task(
            self.start_sender(websocket))

    async def disconnect(self, websocket: WebSocket):
        """Disconnect a websocket."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.sender_tasks[websocket].cancel()
            await self.message_queues[websocket].put(None)
            del self.sender_tasks[websocket]
            del self.message_queues[websocket]

    async def start_diagnose(self, task, report_type, report_source, source_urls, tone, websocket, headers=None):
        """Start streaming the output."""
        tone = Tone[tone]
        # add customized JSON config file path here
        config_path = "default"
        report = await run_agent(task, report_type, report_source, source_urls, tone, websocket, headers=headers, config_path=config_path)
        # Create new Chat Agent whenever a new report is written
        self.chat_agent = ChatAgentWithMemory(report, config_path, headers)
        return report

    async def start_research(self, task, websocket):
        """Start streaming the output."""
        await run_research(task, websocket)
        # Create new Chat Agent whenever a new report is written
        # self.chat_agent = ChatAgentWithMemory(report, config_path, headers)
        # return report

    async def chat(self, message, websocket):
        """Chat with the agent based message diff"""
        if self.chat_agent:
            await self.chat_agent.chat(message, websocket)
        else:
            await websocket.send_json({"type": "chat", "content": "Knowledge empty, please run the research first to obtain knowledge"})


async def run_research(task, websocket = None):
    start_time = datetime.datetime.now()
    print("task", task)
    query = json.loads(task).get('query')
    data = json.loads(task).get('data')
    researcher = GPTResearcher(
        # query=self.query,
        # query=f"how {topic} relate to mental health",
        # report_type=self.report_type,
        # report_source=self.report_source,
        # source_urls=self.source_urls,
        # tone=self.tone,
        # config_path=self.config_path,
        # websocket=self.websocket,
        # headers=self.headers
    )
    if data:
        await researcher.conduct_data_research(data)
    else:
        topics = query.split(";")
        report = ''
        # for topic in topics:
        for topic in topics:
            if topic:
                print("Topic: ", topic)
                #await researcher.conduct_research(f"how {topic.strip()} relate to mental health")
                await researcher.conduct_research(topic.strip())

    end_time = datetime.datetime.now()
    if websocket:
        await websocket.send_json(
            {"type": "logs", "output": f"\nTotal run time: {end_time - start_time}\n"}
        )

    #return report

async def run_agent(task, report_type, report_source, source_urls, tone: Tone, websocket, headers=None, config_path=""):
    """Run the agent."""
    start_time = datetime.datetime.now()
    # Instead of running the agent directly run it through the different report type classes
    if report_type == "multi_agents":
        report = await run_research_task(query=task, websocket=websocket, stream_output=stream_output, tone=tone, headers=headers)
        report = report.get("report", "")
    else:
        researcher = BasicReport(
            query=task,
            report_type=report_type,
            report_source=report_source,
            source_urls=source_urls,
            tone=tone,
            config_path=config_path,
            websocket=websocket,
            headers=headers
        )
        report = await researcher.run()
    '''elif report_type == ReportType.DetailedReport.value:
        researcher = DetailedReport(
            query=task,
            report_type=report_type,
            report_source=report_source,
            source_urls=source_urls,
            tone=tone,
            config_path=config_path,
            websocket=websocket,
            headers=headers
        )
        report = await researcher.run()'''

    # measure time
    end_time = datetime.datetime.now()
    await websocket.send_json(
        {"type": "logs", "output": f"\nTotal run time: {end_time - start_time}\n"}
    )

    return report
