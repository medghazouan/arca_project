import React from 'react';
import { IoArrowForward } from 'react-icons/io5';
import logoImage from '../assets/logo.png';

const Hero = ({ onNavigate }) => {
    return (
        <div className="relative overflow-hidden bg-gradient-to-b from-slate-50 to-white min-h-screen flex items-center">
            {/* Animated Background Elements */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute top-20 left-10 w-72 h-72 bg-blue-400/20 rounded-full blur-3xl animate-pulse"></div>
                <div className="absolute bottom-20 right-10 w-96 h-96 bg-cyan-400/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-purple-400/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
            </div>

            {/* Subtle Background Pattern */}
            <div className="absolute inset-0 opacity-5">
                <div className="absolute inset-0" style={{
                    backgroundImage: 'radial-gradient(circle at 2px 2px, rgb(71, 85, 105) 1px, transparent 0)',
                    backgroundSize: '40px 40px'
                }}></div>
            </div>

            {/* Content */}
            <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                <div className="text-center space-y-8">
                    {/* Logo with Float Animation */}
                    <div className="inline-block animate-float">
                        <div className="relative">
                            <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
                            <img
                                src={logoImage}
                                alt="ARCA Logo"
                                className="w-32 h-32 mx-auto relative z-10 drop-shadow-lg transition-transform duration-500 hover:scale-110 hover:rotate-6"
                            />
                        </div>
                    </div>

                    {/* Heading with Fade In */}
                    <div className="space-y-4 animate-fadeInUp">
                        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
                            <span className="block text-slate-900">
                                Regulatory Compliance
                            </span>
                            <span className="block mt-2">
                                <span className="text-slate-900">Agent </span>
                                <span className="bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-600 bg-clip-text text-transparent animate-gradient bg-[length:200%_auto]">
                                    Reimagined
                                </span>
                            </span>
                        </h1>

                        <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
                            Automate your compliance with artificial intelligence
                        </p>
                    </div>

                    {/* CTA Button with Animation */}
                    <div className="pt-4 animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
                        <button
                            onClick={onNavigate}
                            className="group inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 transition-all duration-300 hover:-translate-y-1 hover:scale-105"
                        >
                            <span>Get Started</span>
                            <IoArrowForward className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
                        </button>
                    </div>

                    {/* Floating Badges */}
                    <div className="flex items-center justify-center gap-6 pt-8 animate-fadeInUp" style={{ animationDelay: '0.4s' }}>
                        <div className="flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full shadow-md border border-slate-200 animate-float" style={{ animationDelay: '0.5s' }}>
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                            <span className="text-sm font-medium text-slate-700">AI Powered</span>
                        </div>
                        <div className="flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full shadow-md border border-slate-200 animate-float" style={{ animationDelay: '1s' }}>
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                            <span className="text-sm font-medium text-slate-700">Real-time Analysis</span>
                        </div>
                    </div>
                </div>
            </div>

            <style jsx>{`
                @keyframes float {
                    0%, 100% {
                        transform: translateY(0px);
                    }
                    50% {
                        transform: translateY(-20px);
                    }
                }

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

                @keyframes gradient {
                    0% {
                        background-position: 0% center;
                    }
                    50% {
                        background-position: 100% center;
                    }
                    100% {
                        background-position: 0% center;
                    }
                }

                .animate-float {
                    animation: float 3s ease-in-out infinite;
                }

                .animate-fadeInUp {
                    animation: fadeInUp 0.8s ease-out forwards;
                    opacity: 0;
                }

                .animate-gradient {
                    animation: gradient 3s ease infinite;
                }
            `}</style>
        </div>
    );
};

export default Hero;