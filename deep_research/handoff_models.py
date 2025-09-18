from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class HandoffType(str, Enum):
    """Types of handoffs available in the research system"""
    HUMAN_REVIEW = "human_review"
    EXPERT_CONSULTATION = "expert_consultation"
    ADDITIONAL_RESEARCH = "additional_research"
    QUALITY_CHECK = "quality_check"
    APPROVAL = "approval"
    CUSTOM = "custom"

class ResearchContext(BaseModel):
    """Context information passed during handoffs"""
    original_query: str = Field(description="The original research query")
    current_stage: str = Field(description="Current stage of research (planning, searching, writing, etc.)")
    search_results: Optional[List[str]] = Field(default=None, description="Search results if available")
    draft_report: Optional[str] = Field(default=None, description="Draft report if available")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class HumanReviewRequest(BaseModel):
    """Request for human review during research process"""
    handoff_type: HandoffType = Field(default=HandoffType.HUMAN_REVIEW)
    context: ResearchContext = Field(description="Research context")
    review_prompt: str = Field(description="What the human should review")
    options: List[str] = Field(description="Available options for the human to choose")
    timeout_minutes: int = Field(default=30, description="Timeout for human response")

class ExpertConsultationRequest(BaseModel):
    """Request for expert consultation"""
    handoff_type: HandoffType = Field(default=HandoffType.EXPERT_CONSULTATION)
    context: ResearchContext = Field(description="Research context")
    expert_domain: str = Field(description="Domain of expertise needed")
    specific_questions: List[str] = Field(description="Specific questions for the expert")
    urgency: str = Field(default="normal", description="Urgency level: low, normal, high")

class AdditionalResearchRequest(BaseModel):
    """Request for additional research"""
    handoff_type: HandoffType = Field(default=HandoffType.ADDITIONAL_RESEARCH)
    context: ResearchContext = Field(description="Research context")
    additional_searches: List[str] = Field(description="Additional search terms needed")
    research_focus: str = Field(description="Focus area for additional research")
    depth_level: str = Field(default="standard", description="Research depth: shallow, standard, deep")

class QualityCheckRequest(BaseModel):
    """Request for quality check"""
    handoff_type: HandoffType = Field(default=HandoffType.QUALITY_CHECK)
    context: ResearchContext = Field(description="Research context")
    check_type: str = Field(description="Type of quality check needed")
    criteria: List[str] = Field(description="Quality criteria to check against")

class ApprovalRequest(BaseModel):
    """Request for approval to proceed"""
    handoff_type: HandoffType = Field(default=HandoffType.APPROVAL)
    context: ResearchContext = Field(description="Research context")
    approval_for: str = Field(description="What needs approval")
    alternatives: Optional[List[str]] = Field(default=None, description="Alternative options")

class HandoffResponse(BaseModel):
    """Response from handoff recipient"""
    approved: bool = Field(description="Whether the request was approved")
    response_data: Dict[str, Any] = Field(description="Response data from handoff recipient")
    next_action: str = Field(description="Next action to take")
    modifications: Optional[Dict[str, Any]] = Field(default=None, description="Any modifications requested")
    additional_instructions: Optional[str] = Field(default=None, description="Additional instructions")
