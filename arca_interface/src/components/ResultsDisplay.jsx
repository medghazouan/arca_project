import React from 'react';
import { MdDescription, MdAccessTime, MdDownload, MdClose, MdTrendingUp, MdAutoAwesome } from 'react-icons/md';
import { HiSparkles, HiLightningBolt } from 'react-icons/hi';
import { IoFlameSharp, IoShieldCheckmark, IoRocketSharp, IoBulbSharp } from 'react-icons/io5';
import { RiAlertFill } from 'react-icons/ri';
import { FaSkull, FaExclamationTriangle, FaCheckCircle } from 'react-icons/fa';

const ResultsDisplay = ({ result, error, loading, onClearError, onDownload }) => {
    const getSeverityColor = (severity) => {
        const colors = {
            HIGH: 'from-red-500 to-pink-500',
            MEDIUM: 'from-yellow-500 to-orange-500',
            LOW: 'from-blue-500 to-cyan-500'
        };
        return colors[severity] || 'from-gray-500 to-gray-600';
    };

    const getSeverityBadgeColor = (severity) => {
        const colors = {
            HIGH: 'bg-red-100 text-red-800 border-red-300',
            MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-300',
            LOW: 'bg-blue-100 text-blue-800 border-blue-300'
        };
        return colors[severity] || 'bg-gray-100 text-gray-800 border-gray-300';
    };

    const getSeverityIcon = (severity) => {
        if (severity === 'HIGH') return <IoFlameSharp className="w-5 h-5 animate-pulse-danger" />;
        if (severity === 'MEDIUM') return <HiLightningBolt className="w-5 h-5 animate-bounce-subtle" />;
        return <IoShieldCheckmark className="w-5 h-5" />;
    };

    // Sort risks by severity: HIGH -> MEDIUM -> LOW
    const sortedRisks = result?.risks ? [...result.risks].sort((a, b) => {
        const severityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
        return severityOrder[a.severity] - severityOrder[b.severity];
    }) : [];

    if (error) {
        return (
            <div className="bg-red-50 border-2 border-red-200 rounded-3xl p-6 mb-6 flex items-start animate-slideIn shadow-lg">
                <FaSkull className="w-6 h-6 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
                <div className="flex-1">
                    <h3 className="text-lg font-bold text-red-900">Analysis Error</h3>
                    <p className="text-sm text-red-700 mt-1">{error}</p>
                </div>
                <button onClick={onClearError} className="ml-auto hover:bg-red-100 rounded-lg p-2 transition-colors duration-200">
                    <MdClose className="w-5 h-5 text-red-600" />
                </button>
            </div>
        );
    }

    if (!result && !loading) {
        return (
            <div className="bg-white rounded-3xl shadow-2xl border border-slate-200 p-12 text-center animate-fadeInUp">
                <div className="w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 bg-gradient-to-br from-blue-500 to-cyan-500 shadow-xl animate-pulse">
                    <IoRocketSharp className="w-12 h-12 text-white" />
                </div>
                <h3 className="text-3xl font-bold mb-3 text-slate-900">Ready to Analyze</h3>
                <p className="text-slate-600">
                    Enter regulation text or upload a document to begin compliance analysis
                </p>
            </div>
        );
    }

    if (!result) return null;

    return (
        <div className="space-y-8">
            {/* Header Section */}
            <div className="relative group animate-fadeInUp">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-600 rounded-3xl opacity-30 group-hover:opacity-50 blur-lg transition-all duration-500"></div>
                <div className="relative bg-white rounded-3xl shadow-2xl border border-slate-200 p-8">
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <div className="flex items-center gap-3 mb-4 animate-slideInLeft">
                                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center shadow-lg hover:scale-110 transition-transform duration-300 hover:rotate-12">
                                    <MdAutoAwesome className="w-7 h-7 text-white" />
                                </div>
                                <div>
                                    <h2 className="text-3xl font-bold text-slate-900">
                                        {result.regulation_title}
                                    </h2>
                                </div>
                            </div>
                            <div className="flex items-center space-x-4 text-sm font-semibold text-slate-600 animate-fadeIn" style={{ animationDelay: '0.2s' }}>
                                <span className="bg-slate-100 px-3 py-1 rounded-full hover:bg-slate-200 transition-colors duration-200">ID: {result.regulation_id}</span>
                                <span>•</span>
                                <span className="bg-slate-100 px-3 py-1 rounded-full hover:bg-slate-200 transition-colors duration-200">Effective: {result.date_of_law}</span>
                            </div>
                        </div>
                        <button
                            onClick={onDownload}
                            className="group/btn relative px-6 py-3 rounded-xl text-sm font-semibold transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/30 transform hover:-translate-y-1 flex items-center gap-2 overflow-hidden animate-fadeIn"
                            style={{ animationDelay: '0.3s' }}
                        >
                            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600"></div>
                            <MdDownload className="w-4 h-4 relative z-10 text-white group-hover/btn:scale-110 transition-transform duration-300" />
                            <span className="relative z-10 text-white">Download</span>
                        </button>
                    </div>
                </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                    {
                        label: 'Total Risks',
                        value: result.total_risks_flagged,
                        icon: FaExclamationTriangle,
                        gradient: 'from-red-500 to-pink-500'
                    },
                    {
                        label: 'Policies Analyzed',
                        value: result.metadata?.total_policies_analyzed || 0,
                        icon: IoBulbSharp,
                        gradient: 'from-purple-500 to-indigo-500'
                    },
                    {
                        label: 'Date Processed',
                        value: result.date_processed,
                        icon: MdAccessTime,
                        gradient: 'from-green-500 to-emerald-500',
                        isDate: true
                    }
                ].map((card, index) => (
                    <div
                        key={index}
                        className="relative group animate-scaleIn"
                        style={{ animationDelay: `${0.1 * (index + 1)}s` }}
                    >
                        <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-2xl opacity-20 group-hover:opacity-40 blur transition-all duration-500"></div>
                        <div className="relative bg-white rounded-2xl shadow-lg border border-slate-200 p-6 hover:scale-105 hover:shadow-xl transition-all duration-300">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-semibold text-slate-600 mb-2">{card.label}</p>
                                    <p className="text-4xl font-bold text-slate-900">
                                        {card.isDate ? new Date(card.value).toLocaleDateString() : card.value}
                                    </p>
                                </div>
                                <div className={`p-4 rounded-xl bg-gradient-to-br ${card.gradient} shadow-lg group-hover:scale-110 group-hover:rotate-12 transition-all duration-300`}>
                                    <card.icon className="w-7 h-7 text-white" />
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Risk Cards Section */}
            <div className="space-y-6">
                <div className="flex items-center gap-3 animate-fadeInUp" style={{ animationDelay: '0.4s' }}>
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-red-500 to-pink-500 flex items-center justify-center shadow-lg animate-pulse-danger">
                        <IoFlameSharp className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-3xl font-bold text-slate-900">Identified Risks</h3>
                    <span className="text-sm text-slate-500 font-semibold">(Sorted by severity)</span>
                </div>
                {sortedRisks.map((risk, index) => (
                    <div
                        key={index}
                        className="relative group animate-fadeInUp"
                        style={{ animationDelay: `${0.5 + (index * 0.1)}s` }}
                    >
                        <div className={`absolute -inset-0.5 bg-gradient-to-r ${getSeverityColor(risk.severity)} rounded-3xl opacity-20 group-hover:opacity-30 blur transition-all duration-500`}></div>

                        <div className="relative bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden hover:shadow-2xl transition-all duration-300">
                            {/* Risk Header */}
                            <div className={`px-8 py-6 ${risk.severity === 'HIGH' ? 'bg-gradient-to-br from-red-50 to-pink-50 border-b border-red-200' :
                                risk.severity === 'MEDIUM' ? 'bg-gradient-to-br from-yellow-50 to-orange-50 border-b border-yellow-200' :
                                    'bg-gradient-to-br from-blue-50 to-cyan-50 border-b border-blue-200'
                                }`}>
                                <div className="flex items-start justify-between">
                                    <div className="flex items-start space-x-4">
                                        <div className={`p-3 rounded-xl bg-gradient-to-br ${getSeverityColor(risk.severity)} shadow-lg hover:scale-110 hover:rotate-6 transition-all duration-300`}>
                                            {getSeverityIcon(risk.severity)}
                                            <div className="text-white"></div>
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-xl text-slate-900 mb-2">
                                                {risk.policy_id}
                                            </h4>
                                            <span className={`inline-block px-4 py-1.5 rounded-full text-xs font-bold border ${getSeverityBadgeColor(risk.severity)}`}>
                                                {risk.severity} SEVERITY
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="p-8 space-y-6">
                                <div className="animate-fadeIn" style={{ animationDelay: `${0.6 + (index * 0.1)}s` }}>
                                    <h5 className="text-sm font-bold mb-3 text-slate-700 uppercase tracking-wider flex items-center gap-2">
                                        <RiAlertFill className="w-4 h-4" />
                                        Divergence Summary
                                    </h5>
                                    <p className="text-base text-slate-700 leading-relaxed">
                                        {risk.divergence_summary}
                                    </p>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-2xl p-5 border border-slate-200 hover:shadow-md transition-all duration-300 animate-slideInLeft" style={{ animationDelay: `${0.7 + (index * 0.1)}s` }}>
                                        <h5 className="text-sm font-bold mb-3 text-slate-900 uppercase tracking-wide flex items-center gap-2">
                                            <MdDescription className="w-4 h-4" />
                                            Current Policy Excerpt
                                        </h5>
                                        <p className="text-sm text-slate-600 italic leading-relaxed">
                                            {risk.conflicting_policy_excerpt}
                                        </p>
                                    </div>
                                    <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl p-5 border border-blue-200 hover:shadow-md transition-all duration-300 animate-slideInRight" style={{ animationDelay: `${0.7 + (index * 0.1)}s` }}>
                                        <h5 className="text-sm font-bold mb-3 text-blue-900 uppercase tracking-wide flex items-center gap-2">
                                            <HiSparkles className="w-4 h-4" />
                                            New Regulation Excerpt
                                        </h5>
                                        <p className="text-sm text-slate-700 leading-relaxed">
                                            {risk.new_rule_excerpt}
                                        </p>
                                    </div>
                                </div>

                                <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-2xl p-6 hover:shadow-md transition-all duration-300 animate-fadeIn" style={{ animationDelay: `${0.8 + (index * 0.1)}s` }}>
                                    <h5 className="text-sm font-bold text-green-900 mb-3 flex items-center uppercase tracking-wide">
                                        <MdTrendingUp className="w-5 h-5 mr-2" />
                                        Recommendation
                                    </h5>
                                    <p className="text-base text-green-800 leading-relaxed">{risk.recommendation}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <style jsx>{`
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                @keyframes slideInLeft {
                    from { opacity: 0; transform: translateX(-30px); }
                    to { opacity: 1; transform: translateX(0); }
                }
                @keyframes slideInRight {
                    from { opacity: 0; transform: translateX(30px); }
                    to { opacity: 1; transform: translateX(0); }
                }
                @keyframes scaleIn {
                    from { opacity: 0; transform: scale(0.9); }
                    to { opacity: 1; transform: scale(1); }
                }
                @keyframes slideIn {
                    from { opacity: 0; transform: translateY(-20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes pulse-danger {
                    0%, 100% { 
                        opacity: 1;
                        transform: scale(1);
                    }
                    50% { 
                        opacity: 0.8;
                        transform: scale(1.05);
                    }
                }
                @keyframes bounce-subtle {
                    0%, 100% {
                        transform: translateY(0);
                    }
                    50% {
                        transform: translateY(-3px);
                    }
                }
                
                .animate-fadeInUp { animation: fadeInUp 0.8s ease-out forwards; opacity: 0; }
                .animate-fadeIn { animation: fadeIn 0.6s ease-out forwards; opacity: 0; }
                .animate-slideInLeft { animation: slideInLeft 0.7s ease-out forwards; opacity: 0; }
                .animate-slideInRight { animation: slideInRight 0.7s ease-out forwards; opacity: 0; }
                .animate-scaleIn { animation: scaleIn 0.6s ease-out forwards; opacity: 0; }
                .animate-slideIn { animation: slideIn 0.5s ease-out forwards; }
                .animate-pulse-danger { animation: pulse-danger 2s ease-in-out infinite; }
                .animate-bounce-subtle { animation: bounce-subtle 1.5s ease-in-out infinite; }
            `}</style>
        </div>
    );
};

export default ResultsDisplay;
