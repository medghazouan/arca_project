import React from 'react';
import { useNavigate } from 'react-router-dom';
import Hero from '../components/Hero';
import Footer from '../components/Footer';
import Team from '../components/Team';


const HomePage = () => {
    const navigate = useNavigate();

    const handleNavigate = () => {
        navigate('/analyzer');
    };

    return (
        <div className="min-h-screen">
            <Hero onNavigate={handleNavigate} />
            
            <Team />
            <Footer />
        </div>
    );
};

export default HomePage;
