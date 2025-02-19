from ...utils.med_agent.llm import construct_med_groups, construct_med_names
from ..writer import ReportGenerator
from gpt_researcher.actions.diagnose_agent import generate_report

class DiagnoseReportGenerator(ReportGenerator):
    async def write_report(self, query, ext_context=None) -> str:
        from gpt_researcher import actions

        actions.generate_report = generate_report
        return await super(DiagnoseReportGenerator, self).write_report(query, ext_context)
