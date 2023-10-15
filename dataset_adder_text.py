import json 
from dataclasses import dataclass, field
from typing import List
import copy


@dataclass
class Step:
    action: str = ""
    arguments: List[str] = field(default_factory=list)

@dataclass
class Task:
    plan_id: int = -1
    goal_eng: str = ""
    plan: List[Step] = field(default_factory=list)
    image: str = ""
    task_type: int = 0


class DatasetAdder:
    
    def __init__(self) -> None:
        self.special = ('unspecified')
    
    def _create_objects(self) -> None:
        movable_obj = set()
        non_movable_obj = set()
        for i in self.json_data:
            for j in i.get('plan'):
                if not j[1][1] == self.special[0]:
                    movable_obj.add(j[1][1])
                if not j[1][0] == self.special[0]:
                    non_movable_obj.add(j[1][0])
                
        self.movable_objs = tuple(movable_obj)
        self.non_movable_obj = tuple(non_movable_obj)
        
        
    def _change_obj(self, task:Task, new_obj:str, *, movable:bool) -> Task:
        
        if movable:
            movable_obj = False
            for i in task.plan:
                if not i.arguments[1] in self.special:
                    movable_obj = i.arguments[1]
                    break
            
            if movable_obj:
                for i in task.plan:
                    if not i.arguments[1] in self.special:
                        i.arguments[1] = new_obj
                
                task.goal_eng = task.goal_eng.replace(movable_obj, new_obj)
                return task
        else:
            non_movable_obj = False
            for i in task.plan:
                if not i.arguments[0] in self.special:
                    continue
            
            if non_movable_obj:
                return None
                
            return None
        
        
    def _writhh(self, tasks:list[Task], *, path:str='./') -> None:
        data = []
        for index, i in enumerate(tasks):
            data.append({'plan_id':i.plan_id, 
                         'image':i.image, 
                         'additional_image':[f'new_images/{i.image}']+[f'new_images/{"".join(i.image.split(".png")[:-1])}_{g}.png' for g in range(11)], 
                         'goal_eng':i.goal_eng, 
                         'task_type':i.task_type, 
                         'id':index})
            
            data[-1]['plan'] = []
            
            for step in i.plan:
                data[-1]['plan'].append([step.action, step.arguments])
                
        with open(f'{path.split(".")[-1]}_new.json', 'w+', encoding='UTF-8') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
        
         
    def _remove_duplicates(self, tasks: list[Task]) -> None:
        tasks_new = []
        for task in tasks:
            if not task in tasks_new:
                tasks_new.append(task)
                
        return tasks_new
        
    
    def _create_tasks_list(self, root_tasks:list[Task]) -> list[Task]:
        taskss = [*root_tasks]
        for task in copy.deepcopy(root_tasks):
            for obj in self.movable_objs:
                res = self._change_obj(copy.deepcopy(task), obj, movable=True)
                if not res is None:
                    taskss.append(res)

        return taskss
    
    
    def dataset_adder(self, path:str) -> None:
        with open(path, 'r') as f:
            data = json.load(f)
            
        self.json_data = [i for i in data if i.get('plan_id')]
        
        self._create_objects()
        
        tasks = []
        for i in self.json_data:
            steps = []
            for j in i.get('plan'):
                step = Step(j[0], j[1])
                steps.append(step)
            task = Task(i.get('plan_id'), i.get('goal_eng'), steps, i.get('image'), i.get('task_type'))
            tasks.append(task)
            
        
        tasks = self._create_tasks_list(tasks)

        tasks = self._remove_duplicates(tasks)
                
        self._writhh(tasks, path=path)
    
    
def main():
    test = DatasetAdder()  
    test.dataset_adder('train_dataset\\train_dataset.json')
    
if __name__=='__main__':
    main()



