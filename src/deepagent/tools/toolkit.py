import docker
from pydantic import BaseModel, Field
from typing import List
from langchain_core.tools import StructuredTool
from langchain_core.tools.base import BaseTool


class DockerSandboxToolKit:
    def __init__(self, image : str):
        self.client = docker.from_env()
        self.image = image
    
    def execute(self, command: str) -> str:
        """Ejecuta comando dentro del contenedor"""
        container = self.client.containers.run(
            image=self.image,
            command=["bash", "-c", command],
            working_dir="/workspace",
        )
        return container.decode()
    
    class Execute(BaseModel):
        command : str = Field(description="Comando bash para ser ejecutado")


    def get_tools(self) -> List[BaseTool]:
        tools = [
            StructuredTool.from_function(
                name="execute",
                description="Ejecutar comando bash",
                func=self.execute,
                args_schema=self.Execute
            )
        ]
        
        return tools
    
    

if __name__=="__main__":

    toolkit = DockerSandboxToolKit()
    tools = toolkit.get_tools()   
    tool = tools[0]

    response = tool.invoke({"command":"pip install numpy"})
    print(response)
        


"""
python3 -m src.deepagent.tools.toolkit

"""