import yaml
from agents.router_agent import RouterAgent
from agents.aggregator_agent import AggregatorAgent
from agents.domains.course_agent import CourseAgent
from agents.domains.scholarship_agent import ScholarshipAgent

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    course_agent = CourseAgent("config/settings.yaml")
    scholarship_agent = ScholarshipAgent("config/settings.yaml")
    agents = {
        "course": course_agent,
        "scholarship": scholarship_agent
    }

    router = RouterAgent("config/settings.yaml")
    aggregator = AggregatorAgent(agents)

    query = input("Nhập câu hỏi của bạn: ")
    route_info = router.route(query)
    domains = route_info.get("domains", [])
    result = aggregator.aggregate(query, domains)
    print("Kết quả:", result)

if __name__ == "__main__":
    main()