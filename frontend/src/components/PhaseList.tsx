import React, { useState } from 'react';

interface Phase {
  id: number;
  name: string;
  description?: string;
  tasks: Task[];
}

interface Task {
  id: number;
  name: string;
  description?: string;
  status: string;
}

interface PhaseListProps {
  projectId: number;
  phases: Phase[];
  onPhaseAdded: () => void;
  onPhaseUpdated: () => void;
  onPhaseDeleted: () => void;
  onTaskAdded: () => void;
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

const PhaseList: React.FC<PhaseListProps> = ({
  projectId,
  phases,
  onPhaseAdded,
  onPhaseUpdated,
  onPhaseDeleted,
  onTaskAdded,
  onTaskUpdated,
  onTaskDeleted,
}) => {
  const [newPhaseName, setNewPhaseName] = useState('');
  const [newPhaseDescription, setNewPhaseDescription] = useState('');
  const [editingPhase, setEditingPhase] = useState<Phase | null>(null);

  const handleAddPhase = () => {
    fetch(`/api/projects/${projectId}/phases/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: newPhaseName, description: newPhaseDescription }),
    })
      .then(response => response.json())
      .then(() => {
        setNewPhaseName('');
        setNewPhaseDescription('');
        onPhaseAdded();
      });
  };

  const handleUpdatePhase = (phaseId: number) => {
    if (editingPhase) {
      fetch(`/api/phases/${phaseId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: editingPhase.name, description: editingPhase.description }),
      })
        .then(response => response.json())
        .then(() => {
          setEditingPhase(null);
          onPhaseUpdated();
        });
    }
  };

  const handleDeletePhase = (phaseId: number) => {
    fetch(`/api/phases/${phaseId}`, {
      method: 'DELETE',
    })
      .then(() => {
        onPhaseDeleted();
      });
  };

  

  const handleUpdateTask = (taskId: number, taskName: string, taskDescription: string, taskStatus: string) => {
    fetch(`/api/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: taskName, description: taskDescription, status: taskStatus }),
    })
      .then(response => response.json())
      .then(() => {
        onTaskUpdated();
      });
  };

  const handleDeleteTask = (taskId: number) => {
    fetch(`/api/tasks/${taskId}`, {
      method: 'DELETE',
    })
      .then(() => {
        onTaskDeleted();
      });
  };

  return (
    <div className="mt-8">
      <h3 className="text-xl font-bold mb-4">Fáze Projektu</h3>
      <div className="mb-4 p-4 border rounded-lg bg-gray-50">
        <h4 className="font-bold mb-2">Přidat Novou Fázi</h4>
        <input
          type="text"
          placeholder="Název fáze"
          value={newPhaseName}
          onChange={e => setNewPhaseName(e.target.value)}
          className="w-full p-2 border rounded mb-2"
        />
        <textarea
          placeholder="Popis fáze"
          value={newPhaseDescription}
          onChange={e => setNewPhaseDescription(e.target.value)}
          className="w-full p-2 border rounded mb-2"
        />
        <button onClick={handleAddPhase} className="bg-blue-500 text-white px-4 py-2 rounded">Přidat Fázi</button>
      </div>

      {phases.length === 0 ? (
        <p>Žádné fáze nebyly přidány.</p>
      ) : (
        <div>
          {phases.map(phase => (
            <div key={phase.id} className="mb-4 p-4 border rounded-lg bg-white shadow-sm">
              {editingPhase && editingPhase.id === phase.id ? (
                <div>
                  <input
                    type="text"
                    value={editingPhase.name}
                    onChange={e => setEditingPhase({ ...editingPhase, name: e.target.value })}
                    className="w-full p-2 border rounded mb-2"
                  />
                  <textarea
                    value={editingPhase.description || ''}
                    onChange={e => setEditingPhase({ ...editingPhase, description: e.target.value })}
                    className="w-full p-2 border rounded mb-2"
                  />
                  <button onClick={() => handleUpdatePhase(phase.id)} className="bg-green-500 text-white px-3 py-1 rounded mr-2">Uložit</button>
                  <button onClick={() => setEditingPhase(null)} className="bg-gray-500 text-white px-3 py-1 rounded">Zrušit</button>
                </div>
              ) : (
                <div className="flex justify-between items-center mb-2">
                  <div>
                    <h4 className="font-bold text-lg">{phase.name}</h4>
                    {phase.description && <p className="text-sm text-gray-600">{phase.description}</p>}
                  </div>
                  <div>
                    <button onClick={() => setEditingPhase(phase)} className="bg-yellow-500 text-white px-3 py-1 rounded mr-2">Upravit</button>
                    <button onClick={() => handleDeletePhase(phase.id)} className="bg-red-500 text-white px-3 py-1 rounded">Smazat</button>
                  </div>
                </div>
              )}

              {/* Tasks for this phase */}
              <div className="ml-4 mt-4">
                <h5 className="font-bold mb-2">Úkoly:</h5>
                {phase.tasks.length === 0 ? (
                  <p className="text-sm text-gray-600">Žádné úkoly pro tuto fázi.</p>
                ) : (
                  <ul>
                    {phase.tasks.map(task => (
                      <TaskItem
                        key={task.id}
                        task={task}
                        onUpdate={handleUpdateTask}
                        onDelete={handleDeleteTask}
                      />
                    ))}
                  </ul>
                )}
                <AddTaskForm phaseId={phase.id} onTaskAdded={onTaskAdded} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

interface AddTaskFormProps {
  phaseId: number;
  onTaskAdded: () => void;
}

const AddTaskForm: React.FC<AddTaskFormProps> = ({ phaseId, onTaskAdded }) => {
  const [newTaskName, setNewTaskName] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');

  const handleSubmit = () => {
    if (newTaskName.trim() === '') return;
    fetch(`/api/phases/${phaseId}/tasks/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: newTaskName, description: newTaskDescription }),
    })
      .then(response => response.json())
      .then(() => {
        setNewTaskName('');
        setNewTaskDescription('');
        onTaskAdded();
      });
  };

  return (
    <div className="mt-4 p-3 border rounded-lg bg-gray-50">
      <h6 className="font-bold mb-2">Přidat Nový Úkol</h6>
      <input
        type="text"
        placeholder="Název úkolu"
        value={newTaskName}
        onChange={e => setNewTaskName(e.target.value)}
        className="w-full p-2 border rounded mb-2 text-sm"
      />
      <textarea
        placeholder="Popis úkolu"
        value={newTaskDescription}
        onChange={e => setNewTaskDescription(e.target.value)}
        className="w-full p-2 border rounded mb-2 text-sm"
      />
      <button onClick={handleSubmit} className="bg-blue-400 text-white px-3 py-1 rounded text-sm">Přidat Úkol</button>
    </div>
  );
};

interface TaskItemProps {
  task: Task;
  onUpdate: (taskId: number, name: string, description: string, status: string) => void;
  onDelete: (taskId: number) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onUpdate, onDelete }) => {
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const handleUpdate = () => {
    if (editingTask) {
      onUpdate(editingTask.id, editingTask.name, editingTask.description || '', editingTask.status);
      setEditingTask(null);
    }
  };

  return (
    <li className="mb-2 p-2 border rounded bg-gray-100 flex justify-between items-center text-sm">
      {editingTask && editingTask.id === task.id ? (
        <div className="flex-grow">
          <input
            type="text"
            value={editingTask.name}
            onChange={e => setEditingTask({ ...editingTask, name: e.target.value })}
            className="w-full p-1 border rounded mb-1"
          />
          <textarea
            value={editingTask.description || ''}
            onChange={e => setEditingTask({ ...editingTask, description: e.target.value })}
            className="w-full p-1 border rounded mb-1"
          />
          <select
            value={editingTask.status}
            onChange={e => setEditingTask({ ...editingTask, status: e.target.value })}
            className="w-full p-1 border rounded"
          >
            <option value="pending">Čeká</option>
            <option value="in_progress">Probíhá</option>
            <option value="completed">Dokončeno</option>
          </select>
          <div className="mt-2">
            <button onClick={handleUpdate} className="bg-green-500 text-white px-2 py-1 rounded mr-2">Uložit</button>
            <button onClick={() => setEditingTask(null)} className="bg-gray-500 text-white px-2 py-1 rounded">Zrušit</button>
          </div>
        </div>
      ) : (
        <div className="flex-grow">
          <h6 className="font-bold">{task.name} ({task.status})</h6>
          {task.description && <p className="text-xs text-gray-700">{task.description}</p>}
        </div>
      )}
      {!editingTask && (
        <div>
          <button onClick={() => setEditingTask(task)} className="bg-yellow-500 text-white px-2 py-1 rounded mr-2">Upravit</button>
          <button onClick={() => onDelete(task.id)} className="bg-red-500 text-white px-2 py-1 rounded">Smazat</button>
        </div>
      )}
    </li>
  );
};

export default PhaseList;
