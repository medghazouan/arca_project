import React from 'react';
import { MdSecurity } from 'react-icons/md';

const Navigation = ({ onNavigate, currentPage }) => {
    return (
        <nav className="glass sticky top-0 z-50 border-b border-gray-200 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div
                        className="flex items-center space-x-3 cursor-pointer"
                        onClick={() => onNavigate('home')}
                    >
                        <div
                            className="w-10 h-10 rounded-lg flex items-center justify-center"
                            style={{ backgroundColor: '#142336' }}
                        >
                            <MdSecurity className="w-6 h-6 text-white" />
                        </div>
                        <span className="text-2xl font-bold" style={{ color: '#142336' }}>
                            ARCA
                        </span>
                    </div>

                    <button
                        onClick={() => onNavigate('home')}
                        className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                    >
                        ← Back to Home
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navigation;
