import React from 'react';
import hicham from '../assets/team-hicham.png';
import Chaima from '../assets/team-chaima.png';
import Sabah from '../assets/team-sabah.png';
import Yahya from '../assets/team-yahya.png';
import Mohamed from '../assets/team-mohamed.png';
import Ismail from '../assets/team-ismail.png';

const members = [
    { name: 'Hicham Ait El Arouri', role: 'UI/UX Designer', photo: hicham },
    { name: 'Ismail El Amali', role: 'Product Owner', photo: Ismail },
    { name: 'Chaima Drai', role: 'Scrum Master', photo: Chaima },
    { name: 'Sabah Ettaleb', role: 'Project Manager', photo: Sabah },
    { name: 'Yahya Allaoui', role: 'Creative Director', photo: Yahya },
    { name: 'Mohamed Ghazouan', role: 'AI Developer', photo: Mohamed }
];

export default function Team() {
    return (
        <section className="relative bg-gradient-to-b from-white to-slate-50 py-16 lg:py-24 overflow-hidden">
            {/* Animated Background Elements */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute top-10 right-10 w-72 h-72 bg-blue-300/10 rounded-full blur-3xl animate-pulse"></div>
                <div className="absolute bottom-10 left-10 w-72 h-72 bg-cyan-300/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
            </div>

            <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header with Animation */}
                <div className="text-center mb-12 lg:mb-16 animate-fadeInUp">
                    <h2 className="text-3xl lg:text-4xl font-bold text-slate-900 mb-4">
                        Team — <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">Law Watchers</span>
                    </h2>
                    <p className="text-lg text-slate-600 max-w-2xl mx-auto">
                        The team behind ARCA — combining legal expertise with cutting-edge AI development.
                    </p>
                </div>

                {/* Team Grid with Staggered Animation */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
                    {members.map((m, idx) => (
                        <div 
                            key={idx} 
                            className="group bg-white rounded-xl p-6 shadow-sm hover:shadow-lg transition-all duration-500 border border-slate-200 hover:border-blue-300 hover:-translate-y-2 animate-fadeInUp"
                            style={{ animationDelay: `${idx * 0.1}s` }}
                        >
                            <div className="flex items-center gap-4">
                                {/* Photo with Hover Effect */}
                                <div className="relative w-16 h-16 rounded-full overflow-hidden bg-gradient-to-br from-blue-600 to-cyan-600 shrink-0 flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-500 group-hover:scale-110">
                                    {/* Animated Ring */}
                                    <div className="absolute inset-0 rounded-full border-2 border-blue-400 scale-100 group-hover:scale-125 opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
                                    
                                    {m.photo ? (
                                        <img 
                                            src={m.photo} 
                                            alt={m.name} 
                                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" 
                                        />
                                    ) : (
                                        <span className="text-white font-bold text-lg">
                                            {m.name.split(' ').map(n => n[0]).slice(0, 2).join('')}
                                        </span>
                                    )}
                                </div>

                                {/* Info */}
                                <div className="flex-1 min-w-0">
                                    <div className="font-semibold text-slate-900 mb-1 truncate group-hover:text-blue-600 transition-colors duration-300">
                                        {m.name}
                                    </div>
                                    <div className="text-sm text-slate-600">
                                        {m.role}
                                    </div>
                                </div>
                            </div>

                            {/* Bottom Accent Bar */}
                            <div className="mt-4 h-1 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>
                        </div>
                    ))}
                </div>
            </div>

            <style jsx>{`
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(30px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                .animate-fadeInUp {
                    animation: fadeInUp 0.8s ease-out forwards;
                    opacity: 0;
                }
            `}</style>
        </section>
    );
}