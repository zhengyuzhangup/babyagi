from segmapy.const import ROOT, CONFIG_ROOT, DEFAULT_WORKSPACE_ROOT
from segmapy.configs.config import config
from segmapy.agents.task import TaskTree

def main():
    TaskManager = TaskTree()
    OBJECTIVE = input("Please input the objective of the task: ")
    root_task = TaskManager.add_root_task(OBJECTIVE)
    print("Root task added: ", root_task)
    # while :

if __name__ == "__main__":
    main()

