import React from 'react';
import { IoArrowBack } from 'react-icons/io5';

const BackToHome = ({ onNavigate }) => {
    return (
        <button
            onClick={onNavigate}
            className="group fixed top-6 left-6 z-50 flex items-center gap-2 px-5 py-2.5 rounded-full font-semibold text-white shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105 bg-slate-800 hover:bg-slate-700 animate-slideInLeft"
        >
            <IoArrowBack className="w-4 h-4 group-hover:-translate-x-1 transition-transform duration-300" />
            <span>Back to Home</span>

            <style jsx>{`
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
                
                .animate-slideInLeft {
                    animation: slideInLeft 0.5s ease-out forwards;
                }
            `}</style>
        </button>
    );
};

export default BackToHome;