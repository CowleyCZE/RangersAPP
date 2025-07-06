import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import PdfViewer from './PdfViewer';
import PhaseList from './PhaseList';

interface Document {
  id: number;
  filename: string;
  category?: string;
  extracted_data?: { key: string; value: string }[];
}

interface ProgressLog {
  id: number;
  date: string;
  percentage_completed: number;
  notes: string;
}

interface Task {
  id: number;
  name: string;
  description?: string;
  status: string;
}

interface Phase {
  id: number;
  name: string;
  description?: string;
  tasks: Task[];
}

interface Project {
  id: number;
  name: string;
  description: string;
  documents: Document[];
  progress_logs: ProgressLog[];
  phases: Phase[];
}

const ProjectDetail: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [percentageCompleted, setPercentageCompleted] = useState<number>(0);
  const [notes, setNotes] = useState<string>('');
  const [overallProgress, setOverallProgress] = useState<number | null>(null);
  const [editingProgressLog, setEditingProgressLog] = useState<ProgressLog | null>(null);
  const [pdfToView, setPdfToView] = useState<string | null>(null);
  const [filterCategory, setFilterCategory] = useState<string>('');
  const [ocrResult, setOcrResult] = useState<string | null>(null);
  const [extractedData, setExtractedData] = useState<any[]>([]);
  const [aisleCountResult, setAisleCountResult] = useState<any | null>(null);

  const fetchProject = () => {
    fetch(`/api/projects/${projectId}`)
      .then(response => response.json())
      .then(data => setProject(data));
    fetch(`/api/projects/${projectId}/overall_progress/`)
      .then(response => response.json())
      .then(data => setOverallProgress(data.overall_progress));
  };

  useEffect(() => {
    fetchProject();
  }, [projectId]);

  useEffect(() => {
    let url = `/api/projects/${projectId}/documents/`;
    if (filterCategory) {
      url += `?category=${filterCategory}`;
    }
    fetch(url)
      .then(response => response.json())
      .then(data => setProject(prevProject => prevProject ? { ...prevProject, documents: data } : null));
  }, [projectId, filterCategory]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleFileUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
      if (selectedCategory) {
        formData.append('category', selectedCategory);
      }

      fetch(`/api/projects/${projectId}/uploadfile/`, {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          console.log('File uploaded:', data);
          fetchProject(); // Refresh project details to show new document
          setSelectedFile(null);
          setSelectedCategory('');
        });
    }
  };

  const handleProgressSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const method = editingProgressLog ? 'PUT' : 'POST';
    const url = editingProgressLog
      ? `/api/progress_logs/${editingProgressLog.id}`
      : `/api/projects/${projectId}/progress_logs/`;

    fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        date: editingProgressLog ? editingProgressLog.date : new Date().toISOString().split('T')[0], // Current date or existing date
        percentage_completed: percentageCompleted,
        notes: notes,
      }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Progress log saved:', data);
        fetchProject(); // Refresh project details to show new progress log
        setPercentageCompleted(0);
        setNotes('');
        setEditingProgressLog(null);
      });
  };

  const handleDeleteProgress = (logId: number) => {
    fetch(`/api/progress_logs/${logId}`, {
      method: 'DELETE',
    })
      .then(response => {
        if (response.ok) {
          fetchProject(); // Refresh project details
        }
      });
  };

  const handleEditProgress = (log: ProgressLog) => {
    setEditingProgressLog(log);
    setPercentageCompleted(log.percentage_completed);
    setNotes(log.notes);
  };

  const handleViewPdf = (documentId: number) => {
    setPdfToView(`/api/documents/${documentId}/download`);
  };

  const handleOcr = (documentId: number) => {
    fetch(`/api/documents/${documentId}/ocr`, {
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        if (data.ocr_text) {
          setOcrResult(data.ocr_text);
          setExtractedData(data.extracted_data);
        } else {
          setOcrResult('OCR failed or no text found.');
          setExtractedData([]);
        }
      })
      .catch(error => {
        console.error('Error during OCR:', error);
        setOcrResult('Error during OCR.');
      });
  };

  const handleCountAisles = (documentId: number) => {
    fetch(`/api/documents/${documentId}/count_aisles`, {
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        setAisleCountResult(data);
      })
      .catch(error => {
        console.error('Error during aisle counting:', error);
        setAisleCountResult({ num_aisles: 0, message: 'Chyba při počítání uliček.' });
      });
  };

  if (!project) {
    return <div>Loading...</div>;
  }

  // Prepare data for the chart
  const chartData = project.progress_logs
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .map(log => ({
      date: log.date,
      "Procento dokončení": log.percentage_completed,
    }));

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Detail Projektu: {project.name}</h2>
      <p className="mb-4">{project.description}</p>

      {overallProgress !== null && (
        <div className="mb-4">
          <h3 className="text-xl font-bold">Celkový postup: {overallProgress.toFixed(2)}%</h3>
        </div>
      )}

      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">Graf Postupu v Čase</h3>
        {chartData.length === 0 ? (
          <p>Pro zobrazení grafu je potřeba zaznamenat postup.</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={chartData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="Procento dokončení" stroke="#8884d8" activeDot={{ r: 8 }} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <PhaseList
        projectId={parseInt(projectId || '0')}
        phases={project.phases}
        onPhaseAdded={fetchProject}
        onPhaseUpdated={fetchProject}
        onPhaseDeleted={fetchProject}
        onTaskAdded={fetchProject}
        onTaskUpdated={fetchProject}
        onTaskDeleted={fetchProject}
      />

      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">Nahrát Dokument</h3>
        <input type="file" onChange={handleFileChange} className="mb-2" />
        <select value={selectedCategory} onChange={e => setSelectedCategory(e.target.value)} className="w-full p-2 border rounded mb-2">
          <option value="">Vyberte kategorii</option>
          <option value="vykres">Výkres</option>
          <option value="rozpocet">Rozpočet</option>
          <option value="fotodokumentace">Fotodokumentace</option>
          <option value="ostatni">Ostatní</option>
        </select>
        <button onClick={handleFileUpload} className="bg-blue-500 text-white px-4 py-2 rounded mt-2">
          Nahrát
        </button>
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">Nahrané Dokumenty</h3>
        {project.documents.length === 0 ? (
          <p>Žádné dokumenty nebyly nahrány.</p>
        ) : (
          <ul>
            {project.documents.map(doc => (
              <li key={doc.id} className="mb-2 p-2 border rounded flex justify-between items-center">
                <div>
                  <a href={`/api/documents/${doc.id}/download`} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                    {doc.filename}
                  </a>
                  {doc.category && <span className="ml-2 text-sm text-gray-600">({doc.category})</span>}
                </div>
                {doc.filename.toLowerCase().endsWith('.pdf') && (
                  <button onClick={() => handleViewPdf(doc.id)} className="bg-gray-200 text-gray-800 px-2 py-1 rounded ml-2">Náhled</button>
                )}
                {(doc.filename.toLowerCase().endsWith('.png') || doc.filename.toLowerCase().endsWith('.jpg') || doc.filename.toLowerCase().endsWith('.jpeg')) && (
                  <button onClick={() => handleOcr(doc.id)} className="bg-blue-200 text-blue-800 px-2 py-1 rounded ml-2">OCR</button>
                )}
                {(doc.filename.toLowerCase().endsWith('.png') || doc.filename.toLowerCase().endsWith('.jpg') || doc.filename.toLowerCase().endsWith('.jpeg')) && (
                  <button onClick={() => handleCountAisles(doc.id)} className="bg-green-200 text-green-800 px-2 py-1 rounded ml-2">Spočítat uličky</button>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      {pdfToView && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white p-4 rounded-lg max-w-3xl max-h-full overflow-auto relative">
            <button onClick={() => setPdfToView(null)} className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold">X</button>
            <PdfViewer pdfUrl={pdfToView} />
          </div>
        </div>
      )}

      {ocrResult && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white p-4 rounded-lg max-w-3xl max-h-full overflow-auto relative">
            <button onClick={() => setOcrResult(null)} className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold">X</button>
            <h3 className="text-xl font-bold mb-2">Výsledek OCR</h3>
            <pre className="whitespace-pre-wrap text-sm mb-4">{ocrResult}</pre>
            {extractedData.length > 0 && (
              <div>
                <h4 className="text-lg font-bold mb-2">Extrahovaná data:</h4>
                <ul>
                  {extractedData.map((item, index) => (
                    <li key={index}>{item.label}: {item.text}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {aisleCountResult && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white p-4 rounded-lg max-w-3xl max-h-full overflow-auto relative">
            <button onClick={() => setAisleCountResult(null)} className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold">X</button>
            <h3 className="text-xl font-bold mb-2">Počet Uliček</h3>
            <p>{aisleCountResult.message}</p>
          </div>
        </div>
      )}

      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">{editingProgressLog ? 'Upravit Záznam Postupu' : 'Zaznamenat Postup'}</h3>
        <form onSubmit={handleProgressSubmit}>
          <div className="mb-4">
            <label htmlFor="percentage" className="block mb-1">Procento dokončení</label>
            <input
              type="number"
              id="percentage"
              min="0"
              max="100"
              value={percentageCompleted}
              onChange={e => setPercentageCompleted(parseInt(e.target.value))}
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="notes" className="block mb-1">Poznámky</label>
            <textarea
              id="notes"
              value={notes}
              onChange={e => setNotes(e.target.value)}
              className="w-full p-2 border rounded"
            />
          </div>
          <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
            {editingProgressLog ? 'Uložit Změny' : 'Uložit Postup'}
          </button>
          {editingProgressLog && (
            <button type="button" onClick={() => {
              setEditingProgressLog(null);
              setPercentageCompleted(0);
              setNotes('');
            }} className="bg-gray-500 text-white px-4 py-2 rounded ml-2">
              Zrušit
            </button>
          )}
        </form>
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4">Historie Postupu</h3>
        {project.progress_logs.length === 0 ? (
          <p>Žádné záznamy o postupu.</p>
        ) : (
          <ul>
            {project.progress_logs.map(log => (
              <li key={log.id} className="mb-2 p-2 border rounded flex justify-between items-center">
                <div>
                  <p>Datum: {log.date}</p>
                  <p>Dokončeno: {log.percentage_completed}%</p>
                  <p>Poznámky: {log.notes}</p>
                </div>
                <div>
                  <button onClick={() => handleEditProgress(log)} className="bg-yellow-500 text-white px-3 py-1 rounded mr-2">Upravit</button>
                  <button onClick={() => handleDeleteProgress(log.id)} className="bg-red-500 text-white px-3 py-1 rounded">
                    Smazat
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ProjectDetail;
