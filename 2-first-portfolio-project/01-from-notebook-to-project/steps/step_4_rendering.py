from html import escape
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
REPORT_DIR = PROJECT_DIR / "report"
OUTPUT_FILENAME = "job-agent-report.html"
TEMPLATE_PATH = REPORT_DIR / "report-template.html"

SKILL_CATEGORIES = [
    "ai-engineering",
    "machine-learning",
    "programming-languages",
    "frontend",
    "backend",
    "databases",
    "cloud",
    "dev-ops",
    "other",
]


class HtmlRenderingStep:
    def run(self, results):
        print("\n--- Step 4: Rendering HTML report ---")

        cards = []
        for job in results:
            cards.append(self._render_job_card(job))

        html = self._render_page(cards, len(results))

        output_path = REPORT_DIR / OUTPUT_FILENAME
        output_path.write_text(html, encoding="utf-8")
        print(f"Saved report with {len(results)} jobs to {output_path}")

    def _render_job_card(self, job):
        skills_by_category = {}
        for skill in job["skills"]:
            skills_by_category.setdefault(skill["category"], []).append(skill["skill"])

        category_blocks = []
        for category in SKILL_CATEGORIES:
            if category not in skills_by_category:
                continue

            category_class = f"category category-{category}"
            skill_chips = "".join(
                f'<span class="chip">{escape(name)}</span>'
                for name in skills_by_category[category]
            )
            category_blocks.append(
                f'<div class="{category_class}"><h3>{escape(category)}</h3>'
                f'<div class="chips">{skill_chips}</div></div>'
            )

        title = escape(job["title"])
        company = str(job.get("company", "")).strip()
        company_html = f'<p class="company">{escape(company)}</p>' if company else ""
        job_url = escape(job["job_url"], quote=True)

        return f"""
        <article class="card">
            <h2><a href="{job_url}" target="_blank" rel="noopener noreferrer">{title}</a></h2>
            {company_html}
            {"".join(category_blocks)}
        </article>
        """

    def _render_page(self, cards, result_count):
        job_plural = "s" if result_count != 1 else ""
        template = TEMPLATE_PATH.read_text(encoding="utf-8")

        return (
            template
            .replace("{{ result_count }}", str(result_count))
            .replace("{{ job_plural }}", job_plural)
            .replace("{{ job_cards }}", "".join(cards))
        )
