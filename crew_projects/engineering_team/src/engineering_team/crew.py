from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task



@CrewBase
class EngineeringTeam():
    """Enhanced EngineeringTeam crew with comprehensive agent roles"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['product_manager'],
            verbose=True,
        )

    @agent
    def architecture_consultant(self) -> Agent:
        return Agent(
            config=self.agents_config['architecture_consultant'],
            verbose=True,
        )

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )

    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_reviewer'],
            verbose=True,
        )

    @agent
    def security_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_engineer'],
            verbose=True,
        )

    @agent
    def devops_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['devops_engineer'],
            verbose=True,
        )

    @agent
    def performance_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_engineer'],
            verbose=True,
        )

    @agent
    def documentation_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['documentation_engineer'],
            verbose=True,
        )

    @agent
    def ux_ui_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['ux_ui_designer'],
            verbose=True,
        )

    @task
    def product_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['product_analysis_task']
        )

    @task
    def architecture_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['architecture_design_task']
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
        )

    @task
    def code_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_review_task'],
        )

    @task
    def security_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_analysis_task'],
        )

    @task
    def devops_setup_task(self) -> Task:
        return Task(
            config=self.tasks_config['devops_setup_task'],
        )

    @task
    def performance_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['performance_analysis_task'],
        )

    @task
    def documentation_task(self) -> Task:
        return Task(
            config=self.tasks_config['documentation_task'],
        )

    @task
    def ux_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['ux_design_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the enhanced engineering team crew with sequential process"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def sequential_crew(self) -> Crew:
        """Creates a sequential crew for simple projects"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def minimal_crew(self) -> Crew:
        """Creates a minimal crew for simple projects"""
        return Crew(
            agents=[
                self.product_manager(),
                self.engineering_lead(),
                self.backend_engineer(),
                self.test_engineer()
            ],
            tasks=[
                self.product_analysis_task(),
                self.design_task(),
                self.code_task(),
                self.test_task()
            ],
            process=Process.sequential,
            verbose=True,
        )

    def standard_crew(self) -> Crew:
        """Creates a standard crew for medium projects"""
        return Crew(
            agents=[
                self.product_manager(),
                self.architecture_consultant(),
                self.backend_engineer(),
                self.frontend_engineer(),
                self.test_engineer(),
                self.code_reviewer(),
                self.security_engineer()
            ],
            tasks=[
                self.product_analysis_task(),
                self.architecture_design_task(),
                self.design_task(),
                self.code_task(),
                self.frontend_task(),
                self.test_task(),
                self.code_review_task(),
                self.security_analysis_task()
            ],
            process=Process.hierarchical,
            manager_agent=self.engineering_lead(),
            verbose=True,
        )

    def full_crew(self) -> Crew:
        """Creates the full crew for complex projects"""
        # Create agents list without the manager agent
        full_agents = [
            self.product_manager(),
            self.architecture_consultant(),
            self.backend_engineer(),
            self.frontend_engineer(),
            self.test_engineer(),
            self.code_reviewer(),
            self.security_engineer(),
            self.devops_engineer(),
            self.performance_engineer(),
            self.documentation_engineer(),
            self.ux_ui_designer()
        ]
        
        return Crew(
            agents=full_agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.engineering_lead(),
            verbose=True,
        )