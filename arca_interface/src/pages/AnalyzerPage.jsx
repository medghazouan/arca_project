import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AnalyzerForm from '../components/AnalyzerForm';
import ResultsDisplay from '../components/ResultsDisplay';
import BackToHome from '../components/BackToHome';
import Footer from '../components/Footer';
import logoImage from '../assets/logo.png';

const AnalyzerPage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('text');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    new_regulation_text: '',
    date_of_law: '',
    regulation_title: ''
  });
  const [file, setFile] = useState(null);
  const [showLogo, setShowLogo] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const API_BASE_URL = 'http://localhost:8000';

  // Show logo on mount, hide it when scrolling
  useEffect(() => {
    const handleScroll = () => {
      if (!result && window.scrollY > 300) {
        setShowLogo(false);
      } else if (!result) {
        setShowLogo(true);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [result]);

  const handleTextSubmit = (e) => {
    e.preventDefault();
    analyzeRegulation();
  };

  const analyzeRegulation = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    setIsAnalyzing(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });

    try {
      const requestBody = {
        new_regulation_text: formData.new_regulation_text
      };

      if (formData.date_of_law && formData.date_of_law.trim() !== '') {
        requestBody.date_of_law = formData.date_of_law;
      }

      if (formData.regulation_title && formData.regulation_title.trim() !== '') {
        requestBody.regulation_title = formData.regulation_title;
      }

      const response = await fetch(`${API_BASE_URL}/analyze_regulation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setIsAnalyzing(false);
    }
  };

  const handleFileSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setIsAnalyzing(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });

    try {
      const formDataFile = new FormData();
      formDataFile.append('file', file);

      if (formData.date_of_law) formDataFile.append('date_of_law', formData.date_of_law);
      if (formData.regulation_title) formDataFile.append('regulation_title', formData.regulation_title);
      formDataFile.append('summarize', 'true');

      const response = await fetch(`${API_BASE_URL}/analyze_regulation_file`, {
        method: 'POST',
        body: formDataFile,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setIsAnalyzing(false);
    }
  };

  const downloadReport = () => {
    const dataStr = JSON.stringify(result, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `arca_report_${result.regulation_id}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleBackToHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      <BackToHome onNavigate={handleBackToHome} />

      {/* Analyzing State Overlay */}
      {isAnalyzing && (
        <div className="fixed inset-0 z-40 flex flex-col items-center justify-center bg-gradient-to-b from-slate-50 to-white">
          <div className="relative">
            {/* Animated Rings */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-96 h-96 rounded-full border-4 border-blue-300 animate-ping-slow opacity-20"></div>
              <div className="absolute w-80 h-80 rounded-full border-4 border-cyan-300 animate-ping-slower opacity-30"></div>
            </div>

            {/* Logo with Pulse */}
            <img 
              src={logoImage} 
              alt="ARCA Logo" 
              className="w-72 h-72 drop-shadow-2xl animate-pulse-soft relative z-10"
            />
          </div>

          {/* Loading Text */}
          <div className="text-center mt-8 animate-fadeIn">
            <h3 className="text-2xl font-bold text-slate-900 mb-2">Analyzing Regulation</h3>
            <p className="text-slate-600">Please wait while our AI agents process your request...</p>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className={isAnalyzing ? 'opacity-0 pointer-events-none' : 'opacity-100 transition-opacity duration-500'}>
        {/* Logo Section - Fades out but keeps space */}
        {!result && (
          <div className={`flex flex-col items-center justify-center pt-20 pb-12 transition-all duration-500 ${
            showLogo ? 'opacity-100' : 'opacity-0 pointer-events-none'
          }`}>
            <div className="relative">
              <div className="absolute inset-0 bg-blue-300/20 rounded-full blur-3xl animate-pulse"></div>
              <img 
                src={logoImage} 
                alt="ARCA Logo" 
                className="w-48 h-48 relative z-10 drop-shadow-xl hover:scale-105 transition-transform duration-300"
              />
            </div>
          </div>
        )}

        {/* Form Section */}
        {!result && (
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
            <AnalyzerForm
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              formData={formData}
              setFormData={setFormData}
              file={file}
              setFile={setFile}
              loading={loading}
              onTextSubmit={handleTextSubmit}
              onFileSubmit={handleFileSubmit}
            />
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <ResultsDisplay
              result={result}
              error={error}
              loading={loading}
              onClearError={() => setError(null)}
              onDownload={downloadReport}
            />
          </div>
        )}

        {/* Error Display */}
        {error && !isAnalyzing && (
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pb-8 animate-slideIn">
            <div className="bg-red-50 border border-red-200 rounded-2xl p-6 flex items-start shadow-lg">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-red-900">Analysis Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="ml-auto hover:bg-red-100 rounded-lg p-2 transition-colors duration-200"
              >
                <span className="text-red-600 text-xl">×</span>
              </button>
            </div>
          </div>
        )}
      </div>

      <Footer />

      <style jsx>{`
        @keyframes fadeInDown {
          from {
            opacity: 0;
            transform: translateY(-30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes ping-slow {
          0% {
            transform: scale(1);
            opacity: 0.2;
          }
          50% {
            transform: scale(1.1);
            opacity: 0;
          }
          100% {
            transform: scale(1);
            opacity: 0.2;
          }
        }

        @keyframes ping-slower {
          0% {
            transform: scale(1);
            opacity: 0.3;
          }
          50% {
            transform: scale(1.15);
            opacity: 0;
          }
          100% {
            transform: scale(1);
            opacity: 0.3;
          }
        }

        @keyframes pulse-soft {
          0%, 100% {
            opacity: 1;
            transform: scale(1);
          }
          50% {
            opacity: 0.8;
            transform: scale(1.05);
          }
        }

        .animate-fadeInDown {
          animation: fadeInDown 0.8s ease-out forwards;
        }

        .animate-fadeIn {
          animation: fadeIn 0.8s ease-out forwards;
        }

        .animate-slideIn {
          animation: slideIn 0.5s ease-out forwards;
        }

        .animate-ping-slow {
          animation: ping-slow 3s cubic-bezier(0, 0, 0.2, 1) infinite;
        }

        .animate-ping-slower {
          animation: ping-slower 4s cubic-bezier(0, 0, 0.2, 1) infinite;
        }

        .animate-pulse-soft {
          animation: pulse-soft 2s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};

export default AnalyzerPage;
