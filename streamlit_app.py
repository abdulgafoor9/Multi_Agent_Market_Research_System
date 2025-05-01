import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datasets import load_dataset

# Load dataset
ds = load_dataset("kshitizgajurel/Devanagari-Ecommerce-Dataset")

class IndustryResearchAgent:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def search_web(self, query):
        encoded_query = quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            snippets = [div.text for div in soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")]
            return " ".join(snippets[:3])
        except Exception as e:
            return f"Error searching web: {str(e)}"

    def research_company(self, company, industry):
        company_query = f"{company} {industry} company overview strategic focus"
        industry_query = f"{industry} industry trends AI ML 2025"
        company_info = self.search_web(company_query)
        industry_info = self.search_web(industry_query)
        return {
            "company_info": company_info,
            "industry_info": industry_info,
            "focus_areas": self.extract_focus_areas(company_info)
        }

    def extract_focus_areas(self, text):
        keywords = ["customer experience", "supply chain", "operations", "marketing", "sales"]
        found = [kw for kw in keywords if kw.lower() in text.lower()]
        return found if found else ["operations", "customer experience"]

class UseCaseGenerationAgent:
    def __init__(self):
        self.use_case_templates = {
            "Retail": [
                {
                    "name": "Personalized Product Recommendations",
                    "description": "Use ML to analyze customer purchase history and preferences to recommend products, increasing sales and customer satisfaction.",
                    "technologies": ["Recommendation Systems", "ML", "Customer Segmentation"],
                    "reference": "McKinsey: AI in Retail Personalization"
                },
                {
                    "name": "Inventory Optimization",
                    "description": "Leverage AI to predict demand and optimize stock levels, reducing overstock and stockouts.",
                    "technologies": ["Time Series Forecasting", "ML", "GenAI for reporting"],
                    "reference": "Deloitte: AI in Retail Supply Chain"
                },
                {
                    "name": "AI-Powered Customer Support Chatbot",
                    "description": "Implement a GenAI-based chatbot for 24/7 customer support, handling inquiries and returns.",
                    "technologies": ["LLMs", "GenAI", "NLP"],
                    "reference": "Nexocode: AI Chatbots in Retail"
                }
            ]
        }

    def generate_use_cases(self, industry, focus_areas):
        use_cases = self.use_case_templates.get(industry, [])
        filtered = [uc for uc in use_cases if any(fa.lower() in uc["description"].lower() for fa in focus_areas)]
        return filtered if filtered else use_cases[:2]

class ResourceCollectionAgent:
    def __init__(self):
        self.predefined_datasets = {
            "Retail": [
                {
                    "name": "Devanagari-Ecommerce-Dataset",
                    "url": "https://huggingface.co/datasets/kshitizgajurel/Devanagari-Ecommerce-Dataset",
                    "platform": "HuggingFace",
                    "description": "Ecommerce product data in Devanagari script for regional retail analytics."
                },
                {
                    "name": "Online Retail Data Set",
                    "url": "https://www.kaggle.com/datasets/vijayuv/onlineretail",
                    "platform": "Kaggle",
                    "description": "Transactional data from a UK-based online retailer for market basket analysis."
                },
                {
                    "name": "Spark Retail Dataset",
                    "url": "https://github.com/databricks/Spark-The-Definitive-Guide/tree/master/data/retail-data",
                    "platform": "GitHub",
                    "description": "Retail dataset for big data processing with Apache Spark."
                }
            ]
        }

    def search_datasets(self, use_case, industry="Retail"):
        resources = {}
        predefined_datasets = self.predefined_datasets.get(industry, [])
        resources["Predefined"] = [f"{ds['name']}: {ds['url']}" for ds in predefined_datasets]
        for platform in ["Kaggle", "HuggingFace", "GitHub"]:
            platform_datasets = [ds["url"] for ds in predefined_datasets if ds["platform"] == platform]
            resources[platform] = platform_datasets if platform_datasets else ["No link found"]
        return resources

    def save_resources(self, use_cases, filename="resources.md"):
        content = "# Resource Assets\n\n"
        for uc in use_cases:
            content += f"## {uc['name']}\n"
            resources = self.search_datasets(uc)
            for platform, links in resources.items():
                content += f"- **{platform}**: {', '.join(links) if links else 'No link found'}\n"
        with open(filename, "w") as f:
            f.write(content)
        return filename

def main(company="RetailCo", industry="Retail"):
    research_agent = IndustryResearchAgent()
    use_case_agent = UseCaseGenerationAgent()
    resource_agent = ResourceCollectionAgent()

    research_data = research_agent.research_company(company, industry)
    focus_areas = research_data["focus_areas"]
    use_cases = use_case_agent.generate_use_cases(industry, focus_areas)
    resource_file = resource_agent.save_resources(use_cases)

    report = f"# AI Use Case Proposal for {company}\n\n"
    report += "## Industry and Company Overview\n"
    report += f"- **Industry**: {industry}\n"
    report += f"- **Company**: {company}\n"
    report += f"- **Focus Areas**: {', '.join(focus_areas)}\n"
    report += f"- **Industry Trends**: {research_data['industry_info'][:200]}...\n\n"
    report += "## Proposed Use Cases\n"
    for uc in use_cases:
        report += f"### {uc['name']}\n"
        report += f"- **Description**: {uc['description']}\n"
        report += f"- **Technologies**: {', '.join(uc['technologies'])}\n"
        report += f"- **Reference**: {uc['reference']}\n"
        resources = resource_agent.search_datasets(uc)
        report += "- **Resources**:\n"
        for platform, links in resources.items():
            link = links[0] if links else "No link found"
            report += f"  - [{platform}]({link})\n"
    return report, resource_file

if __name__ == "__main__":
    report, resource_file = main()
    with open("proposal.md", "w") as f:
        f.write(report)
    print("Proposal generated: proposal.md")
    print(f"Resources saved: {resource_file}")
