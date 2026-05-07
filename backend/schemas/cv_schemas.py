from pydantic import BaseModel, Field


class SkillExtractionRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Text from which skills should be extracted.",
    )


class SkillExtractionResponse(BaseModel):
    skills: list[str]


class CVMatchRequest(BaseModel):
    cv_text: str = Field(
        ...,
        min_length=1,
        description="Raw CV text pasted by the user.",
    )
    top_n: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of matched jobs to return.",
    )


class CVMatchResult(BaseModel):
    job_id: str | None = None
    title: str | None = None
    company: str | None = None
    location: str | None = None
    category: str | None = None
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    extra_cv_skills: list[str]
    required_skill_count: int
    matched_skill_count: int


class SkillGapRequest(BaseModel):
    cv_text: str = Field(
        ...,
        min_length=1,
        description="Raw CV text pasted by the user.",
    )
    top_n: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of missing skills to return.",
    )


class MissingSkill(BaseModel):
    skill: str
    missing_count: int


class RoadmapItem(BaseModel):
    priority: int
    skill: str
    learning_steps: list[str]
    portfolio_task: str


class SkillGapResponse(BaseModel):
    missing_skills: list[MissingSkill]
    roadmap: list[RoadmapItem]