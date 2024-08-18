# Task storage supporting only a single instance of BabyAGI
from collections import deque
from typing import Dict, List

class SingleTaskListStorage:
    def __init__(self):
        self.tasks = deque([])
        self.task_id_counter = 0

    def append(self, task: Dict):
        self.tasks.append(task)

    def replace(self, tasks: List[Dict]):
        self.tasks = deque(tasks)

    def popleft(self):
        return self.tasks.popleft()

    def is_empty(self):
        return False if self.tasks else True

    def next_task_id(self):
        self.task_id_counter += 1
        return self.task_id_counter

    def get_task_names(self):
        return [t["task_name"] for t in self.tasks]


class Task:
    def __init__(self, task_id: int, task_detail: str):
        self.task_id = task_id
        self.task_detail = task_detail
        self.task_level = 0

    def __str__(self):
        return f"Task {self.task_id}: {self.task_detail}"
    

class TaskNode:
    def __init__(self, task_id: int, task_detail: str, parent_task_id: int=None):
        self.task_id = task_id
        # 父任务id
        self.parent_task_id = parent_task_id
        # 任务详情
        self.task_detail = task_detail
        # 该任务是否执行过
        self.is_executed = False
        self.subtasks = []

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

    def __str__(self, level=0):
        ret = "\t" * level + f"Task {self.task_id}: {self.task_detail}\n"
        for subtask in self.subtasks:
            ret += subtask.__str__(level + 1)
        return ret


class TaskTree:
    def __init__(self):
        self.root = None
        self.task_id_counter = 0

    def next_task_id(self):
        self.task_id_counter += 1
        return self.task_id_counter

    def add_root_task(self, task_detail: str):
        task_id = self.next_task_id()
        self.root = TaskNode(task_id, task_detail)
        return self.root

    def add_subtask(self, parent_task: TaskNode, task_detail: str):
        task_id = self.next_task_id()
        subtask = TaskNode(task_id, task_detail, parent_task.task_id)
        parent_task.add_subtask(subtask)
        return subtask

    def __str__(self):
        if self.root is None:
            return "No tasks in the tree."
        return str(self.root)
    
    def pop_task(self):
        ''' 按执行顺序优先级从任务树中弹出一个未执行的任务 '''
        if not self.root:
            return None

        queue = [self.root]
        print("queue= ", queue)
        while queue:
            current_task: TaskNode = queue.pop(0)
            if not current_task.is_executed:
                current_task.is_executed = True
                return current_task
            queue.extend(current_task.subtasks)
        return None
    
    def get_task_names(self):
        if not self.root:
            return []
        queue = [self.root]
        task_names = []
        while queue:
            current_task: TaskNode = queue.pop(0)
            task_names.append(current_task.task_detail)
            queue.extend(current_task.subtasks)
        return task_names
    
    
if __name__ == "__main__":
    task_tree = TaskTree()

    # 添加根任务
    root_task = task_tree.add_root_task("Complete Project")
    print("root_task= ", root_task)
    print(task_tree.pop_task())
    # # 添加子任务
    subtask1 = task_tree.add_subtask(root_task, "Design Module")
    subtask2 = task_tree.add_subtask(root_task, "Implement Module")
    subtask3 = task_tree.add_subtask(root_task, "Test Module")

    # 添加子任务的子任务
    task_tree.add_subtask(subtask1, "Create UML Diagrams")
    task_tree.add_subtask(subtask1, "Review Design")

    task_tree.add_subtask(subtask2, "Write Code")
    task_tree.add_subtask(subtask2, "Code Review")

    task_tree.add_subtask(subtask3, "Write Test Cases")
    task_tree.add_subtask(subtask3, "Execute Tests")
    print(task_tree.get_task_names())
    # # 打印任务树
    # print("接下来中进行的任务是1：\n",task_tree.pop_task().task_detail)
    # print("接下来中进行的任务是2：\n",task_tree.pop_task().task_detail)
    # print("接下来中进行的任务是3：\n",task_tree.pop_task().task_detail)
    # print("接下来中进行的任务是4：\n",task_tree.pop_task().task_detail)
    # print("接下来中进行的任务是5：\n",task_tree.pop_task().task_detail)

