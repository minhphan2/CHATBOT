from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.router_agent import RouterAgent
from agents.aggregator_agent import AggregatorAgent
from agents.domains.course_agent import CourseAgent
from agents.domains.scholarship_agent import ScholarshipAgent
from agents.domains.subject_agent import SubjectAgent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo các agent domain
course_agent = CourseAgent("config/settings.yaml")
scholarship_agent = ScholarshipAgent("config/settings.yaml")
subject_agent = SubjectAgent("config/settings.yaml") 
agents = {
    "course": course_agent,
    "scholarship": scholarship_agent,
    "subject": subject_agent,
    # Thêm các agent domain khác nếu có
}

# Khởi tạo router và aggregator
router_agent = RouterAgent()
aggregator_agent = AggregatorAgent(agents)

@app.post("/chat/")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "")
    if not question:
        return {"answer": "Bạn chưa nhập câu hỏi!"}

    # 1. Router xác định domain và có cần tổng hợp không
    route_info = router_agent.route(question)
    domains = route_info.get("domains", [])
    need_aggregation = route_info.get("need_aggregation", False)

    # 2. Nếu chỉ 1 domain, gọi agent domain đó
    if len(domains) == 1 and not need_aggregation:
        domain = domains[0]
        agent = agents.get(domain)
        if agent:
            answer = agent.answer(question)
        else:
            answer = f"Không tìm thấy agent cho domain: {domain}"
    else:
        # 3. Nếu nhiều domain hoặc cần tổng hợp, gọi aggregator
        answer = aggregator_agent.aggregate(question, domains)

    return {"answer": answer}