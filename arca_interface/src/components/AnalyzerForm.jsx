import React from 'react';
import { HiCloudUpload } from 'react-icons/hi';
import { MdDescription, MdAnalytics } from 'react-icons/md';
import { IoSearch } from 'react-icons/io5';

const AnalyzerForm = ({
  activeTab,
  setActiveTab,
  formData,
  setFormData,
  file,
  setFile,
  loading,
  onTextSubmit,
  onFileSubmit
}) => {
  return (
    <div className="relative group animate-fadeInUp">
      {/* Animated Gradient Border */}
      <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-600 rounded-3xl opacity-30 group-hover:opacity-50 blur transition-all duration-500 animate-gradient-shift"></div>
      
      <div className="relative bg-white rounded-3xl shadow-2xl overflow-hidden border border-slate-200">
        {/* Header with Animated Gradient */}
        <div className="relative px-8 py-6 overflow-hidden bg-gradient-to-r from-blue-600 to-cyan-600">
          {/* Animated Background Elements */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-cyan-400/10 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '1s' }}></div>
          
          <div className="relative flex items-center justify-between">
            <div className="flex items-center gap-3 animate-slideInLeft">
              <div className="w-12 h-12 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center hover:scale-110 transition-transform duration-300 hover:rotate-6">
                <MdAnalytics className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white">New Analysis</h2>
            </div>
          </div>
        </div>

        {/* Tab Selection with Smooth Transitions */}
        <div className="flex border-b border-slate-200 bg-slate-50">
          <button
            onClick={() => setActiveTab('text')}
            className={`flex-1 px-6 py-4 text-sm font-semibold transition-all duration-300 relative ${
              activeTab === 'text' 
                ? 'text-blue-600 bg-white' 
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            <div className="flex items-center justify-center gap-2">
              <MdDescription className={`w-4 h-4 transition-transform duration-300 ${activeTab === 'text' ? 'scale-110' : ''}`} />
              Text Input
            </div>
            {activeTab === 'text' && (
              <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-t-full animate-expandWidth"></div>
            )}
          </button>

          <button
            onClick={() => setActiveTab('file')}
            className={`flex-1 px-6 py-4 text-sm font-semibold transition-all duration-300 relative ${
              activeTab === 'file' 
                ? 'text-blue-600 bg-white' 
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
            }`}
          >
            <div className="flex items-center justify-center gap-2">
              <HiCloudUpload className={`w-4 h-4 transition-transform duration-300 ${activeTab === 'file' ? 'scale-110' : ''}`} />
              File Upload
            </div>
            {activeTab === 'file' && (
              <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-t-full animate-expandWidth"></div>
            )}
          </button>
        </div>

        {/* Form Content */}
        <div className="p-8">
          {activeTab === 'text' ? (
            <form onSubmit={onTextSubmit} className="space-y-6 animate-fadeIn">
              <div className="animate-slideInUp" style={{ animationDelay: '0.1s' }}>
                <label className="block text-sm font-semibold mb-3 text-slate-700">
                  Regulation Title
                </label>
                <input
                  type="text"
                  value={formData.regulation_title}
                  onChange={(e) => setFormData({ ...formData, regulation_title: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all bg-white text-slate-900 placeholder-slate-400 hover:border-slate-300"
                  placeholder="e.g., Employment Safety Act 2025"
                />
              </div>

              <div className="animate-slideInUp" style={{ animationDelay: '0.2s' }}>
                <label className="block text-sm font-semibold mb-3 text-slate-700">
                  Date of Law
                </label>
                <input
                  type="date"
                  value={formData.date_of_law}
                  onChange={(e) => setFormData({ ...formData, date_of_law: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all bg-white text-slate-900 hover:border-slate-300"
                />
              </div>

              <div className="animate-slideInUp" style={{ animationDelay: '0.3s' }}>
                <label className="block text-sm font-semibold mb-3 text-slate-700">
                  Regulation Text
                </label>
                <textarea
                  value={formData.new_regulation_text}
                  onChange={(e) => setFormData({ ...formData, new_regulation_text: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all bg-white text-slate-900 placeholder-slate-400 hover:border-slate-300"
                  rows={10}
                  placeholder="Paste the complete regulation text here (max 2000 words)..."
                />
                <p className="text-xs text-slate-500 mt-2">
                  {formData.new_regulation_text.split(/\s+/).filter(w => w.length > 0).length} / 2000 words
                </p>
              </div>

              <button
                type="submit"
                disabled={loading || !formData.new_regulation_text}
                className="group relative w-full px-8 py-4 rounded-xl text-base font-semibold transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/30 transform hover:-translate-y-1 flex items-center justify-center gap-3 overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 animate-slideInUp"
                style={{ animationDelay: '0.4s' }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 transition-transform duration-300 group-hover:scale-105"></div>
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white relative z-10"></div>
                    <span className="relative z-10 text-white">Analyzing...</span>
                  </>
                ) : (
                  <>
                    <IoSearch className="w-5 h-5 relative z-10 text-white group-hover:scale-110 transition-transform duration-300" />
                    <span className="relative z-10 text-white">Analyze Regulation</span>
                  </>
                )}
              </button>
            </form>
          ) : (
            <form onSubmit={onFileSubmit} className="space-y-6 animate-fadeIn">
              <div className="animate-slideInUp" style={{ animationDelay: '0.1s' }}>
                <label className="block text-sm font-semibold mb-3 text-slate-700">
                  Regulation Title
                </label>
                <input
                  type="text"
                  value={formData.regulation_title}
                  onChange={(e) => setFormData({ ...formData, regulation_title: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all bg-white text-slate-900 placeholder-slate-400 hover:border-slate-300"
                  placeholder="Auto-detected from filename"
                />
              </div>

              <div className="animate-slideInUp" style={{ animationDelay: '0.2s' }}>
                <label className="block text-sm font-semibold mb-3 text-slate-700">
                  Date of Law
                </label>
                <input
                  type="date"
                  value={formData.date_of_law}
                  onChange={(e) => setFormData({ ...formData, date_of_law: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all bg-white text-slate-900 hover:border-slate-300"
                />
              </div>

              <div className="animate-slideInUp" style={{ animationDelay: '0.3s' }}>
                <label className="block text-sm font-semibold mb-3 text-slate-700">
                  Upload File (PDF or TXT)
                </label>
                <div 
                  className="group/upload border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-blue-500 hover:bg-blue-50/50 transition-all duration-300 cursor-pointer relative overflow-hidden"
                  onClick={() => document.getElementById('file-upload').click()}
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-400/5 to-cyan-400/5 opacity-0 group-hover/upload:opacity-100 transition-opacity duration-300"></div>
                  <input
                    type="file"
                    accept=".pdf,.txt,.md"
                    onChange={(e) => setFile(e.target.files[0])}
                    className="hidden"
                    id="file-upload"
                  />
                  <HiCloudUpload className="w-16 h-16 mx-auto text-slate-400 mb-4 group-hover/upload:text-blue-500 group-hover/upload:scale-110 transition-all duration-300" />
                  {file ? (
                    <p className="text-base font-semibold text-blue-600 animate-fadeIn">{file.name}</p>
                  ) : (
                    <>
                      <p className="text-sm font-semibold text-slate-700 mb-1">Click to upload or drag and drop</p>
                      <p className="text-xs text-slate-500">PDF, TXT or MD (max 10MB)</p>
                    </>
                  )}
                </div>
              </div>

              <button
                type="submit"
                disabled={loading || !file}
                className="group relative w-full px-8 py-4 rounded-xl text-base font-semibold transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/30 transform hover:-translate-y-1 flex items-center justify-center gap-3 overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 animate-slideInUp"
                style={{ animationDelay: '0.4s' }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 transition-transform duration-300 group-hover:scale-105"></div>
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white relative z-10"></div>
                    <span className="relative z-10 text-white">Analyzing...</span>
                  </>
                ) : (
                  <>
                    <IoSearch className="w-5 h-5 relative z-10 text-white group-hover:scale-110 transition-transform duration-300" />
                    <span className="relative z-10 text-white">Analyze Document</span>
                  </>
                )}
              </button>
            </form>
          )}
        </div>

        {/* Info Box */}
        <div className="mx-8 mb-8 rounded-xl p-5 bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-200 relative overflow-hidden group/info animate-fadeInUp" style={{ animationDelay: '0.5s' }}>
          <div className="absolute inset-0 bg-gradient-to-br from-blue-100/50 to-cyan-100/50 opacity-0 group-hover/info:opacity-100 transition-opacity duration-300"></div>
          <h3 className="text-sm font-bold mb-3 text-blue-900 relative z-10">How It Works</h3>
          <ul className="text-xs space-y-2 text-slate-700 relative z-10">
            <li className="flex items-start gap-2 animate-slideInLeft" style={{ animationDelay: '0.6s' }}>
              <span className="text-blue-500 font-bold">1.</span>
              <span>Policy Researcher retrieves relevant policies</span>
            </li>
            <li className="flex items-start gap-2 animate-slideInLeft" style={{ animationDelay: '0.7s' }}>
              <span className="text-cyan-500 font-bold">2.</span>
              <span>Compliance Auditor identifies conflicts</span>
            </li>
            <li className="flex items-start gap-2 animate-slideInLeft" style={{ animationDelay: '0.8s' }}>
              <span className="text-blue-600 font-bold">3.</span>
              <span>Report Generator structures findings</span>
            </li>
          </ul>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
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

        @keyframes slideInLeft {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes slideInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes expandWidth {
          from {
            transform: scaleX(0);
          }
          to {
            transform: scaleX(1);
          }
        }

        @keyframes gradient-shift {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }

        .animate-fadeInUp {
          animation: fadeInUp 0.6s ease-out forwards;
          opacity: 0;
        }

        .animate-fadeIn {
          animation: fadeIn 0.4s ease-out forwards;
        }

        .animate-slideInLeft {
          animation: slideInLeft 0.5s ease-out forwards;
          opacity: 0;
        }

        .animate-slideInUp {
          animation: slideInUp 0.6s ease-out forwards;
          opacity: 0;
        }

        .animate-expandWidth {
          animation: expandWidth 0.3s ease-out forwards;
        }

        .animate-gradient-shift {
          background-size: 200% 200%;
          animation: gradient-shift 3s ease infinite;
        }
      `}</style>
    </div>
  );
};

export default AnalyzerForm;
