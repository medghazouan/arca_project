import React from 'react';
import { FaFacebook, FaXTwitter, FaInstagram } from 'react-icons/fa6';

const Footer = () => {
    return (
        <footer className="relative bg-gradient-to-b from-slate-50 to-white overflow-hidden border-t border-slate-200">
            {/* Animated Background */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl animate-pulse"></div>
                <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-cyan-400/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1.5s' }}></div>
            </div>

            <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Social Section */}
                <div className="text-center mb-8 animate-fadeInUp">
                    <h3 className="text-xl font-semibold mb-6 bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                        Connect With Us
                    </h3>
                    <div className="flex items-center justify-center gap-4">
                        <a
                            href="#"
                            className="group relative w-12 h-12 rounded-lg bg-white border-2 border-slate-200 hover:border-blue-500 hover:bg-gradient-to-br hover:from-blue-600 hover:to-blue-500 flex items-center justify-center transition-all duration-300 hover:scale-110 hover:-rotate-6 overflow-hidden shadow-md hover:shadow-xl"
                            aria-label="Facebook"
                        >
                            {/* Shine Effect */}
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
                            <FaFacebook className="w-5 h-5 text-slate-600 group-hover:text-white transition-colors duration-300 relative z-10" />
                        </a>
                        <a
                            href="#"
                            className="group relative w-12 h-12 rounded-lg bg-white border-2 border-slate-200 hover:border-cyan-500 hover:bg-gradient-to-br hover:from-blue-400 hover:to-cyan-400 flex items-center justify-center transition-all duration-300 hover:scale-110 hover:-rotate-6 overflow-hidden shadow-md hover:shadow-xl"
                            aria-label="Twitter"
                        >
                            {/* Shine Effect */}
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
                            <FaXTwitter className="w-5 h-5 text-slate-600 group-hover:text-white transition-colors duration-300 relative z-10" />
                        </a>
                        <a
                            href="#"
                            className="group relative w-12 h-12 rounded-lg bg-white border-2 border-slate-200 hover:border-pink-500 hover:bg-gradient-to-br hover:from-pink-600 hover:to-purple-600 flex items-center justify-center transition-all duration-300 hover:scale-110 hover:-rotate-6 overflow-hidden shadow-md hover:shadow-xl"
                            aria-label="Instagram"
                        >
                            {/* Shine Effect */}
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
                            <FaInstagram className="w-5 h-5 text-slate-600 group-hover:text-white transition-colors duration-300 relative z-10" />
                        </a>
                    </div>
                </div>

                {/* Copyright */}
                <div className="text-center pt-8 border-t border-slate-200 animate-fadeInUp" style={{ animationDelay: '0.2s' }}>
                    <p className="text-slate-600 text-sm">
                        © 2025 <span className="font-semibold text-slate-900">ARCA</span>. Powered by Multi-Agent AI Technology.
                    </p>
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

                .animate-fadeInUp {
                    animation: fadeInUp 0.8s ease-out forwards;
                    opacity: 0;
                }
            `}</style>
        </footer>
    );
};

export default Footer;