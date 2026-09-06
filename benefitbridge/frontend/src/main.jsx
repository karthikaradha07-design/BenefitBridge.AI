import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import './styles.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const events = ['education','health','housing','farming','business','livelihood','retirement','child','savings','family'];

function App(){
  const [lang,setLang]=useState('en');
  const [tab,setTab]=useState('discover');
  const [profile,setProfile]=useState({age:20,state:'Tamil Nadu',gender:'any',occupation:'student',annual_income:200000,life_events:['education'],family_size:1});
  const [results,setResults]=useState([]);
  const [loading,setLoading]=useState(false);
  const [question,setQuestion]=useState('Which government schemes can help me as a student?');
  const [answer,setAnswer]=useState('');
  const [source,setSource]=useState('');
  const [error,setError]=useState('');

  const t = lang==='ta' ? {brand:'BenefitBridge',tag:'உங்களுக்கு பொருந்தும் அரசு நலத்திட்டங்களை கண்டுபிடிக்கவும்',discover:'திட்டங்களை கண்டுபிடி',assistant:'AI உதவியாளர்',profile:'சுயவிவரம்',find:'எனது நலன்களை கண்டுபிடி',ask:'கேள்',income:'ஆண்டு வருமானம்',age:'வயது',state:'மாநிலம்',occupation:'தொழில்'} : {brand:'BenefitBridge',tag:'Find the government benefits you may be eligible for',discover:'Discover schemes',assistant:'AI Assistant',profile:'My profile',find:'Find my benefits',ask:'Ask AI',income:'Annual income',age:'Age',state:'State',occupation:'Occupation'};

  async function match(){
    setLoading(true);setError('');
    try{const r=await fetch(`${API}/api/match`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(profile)});if(!r.ok)throw new Error('Backend error');const d=await r.json();setResults(d.results);setTab('discover')}catch(e){setError('Backend is not running. Start FastAPI on port 8000.')}finally{setLoading(false)}
  }
  async function ask(){
    setLoading(true);setError('');
    try{const r=await fetch(`${API}/api/ask`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,profile})});if(!r.ok)throw new Error('Backend error');const d=await r.json();setAnswer(d.answer);setSource(d.source);setResults(d.results||[]);setTab('assistant')}catch(e){setError('Could not connect to the backend.')}finally{setLoading(false)}
  }
  function toggleEvent(e){setProfile(p=>({...p,life_events:p.life_events.includes(e)?p.life_events.filter(x=>x!==e):[...p.life_events,e]}))}
  return <div className="app">
    <header className="top"><div className="brand"><div className="logo">B</div><div><b>{t.brand}</b><span>{t.tag}</span></div></div><div className="top-actions"><button className="lang" onClick={()=>setLang(lang==='en'?'ta':'en')}>{lang==='en'?'தமிழ்':'English'}</button><span className="verified">● Verified-first</span></div></header>
    <section className="hero"><div className="hero-copy"><p className="eyebrow">AI • ELIGIBILITY • OFFICIAL SOURCES</p><h1>One profile.<br/><em>Right benefits.</em></h1><p>BenefitBridge combines explainable eligibility matching, Qdrant retrieval and Lyzr AI to guide citizens toward relevant government schemes.</p><div className="hero-buttons"><button className="primary" onClick={match}>{loading?'Matching…':t.find} <span>→</span></button><button className="secondary" onClick={()=>setTab('assistant')}>{t.assistant}</button></div></div><div className="hero-card"><div className="orb">₹</div><div><strong>Benefit match engine</strong><p>Profile → Qdrant → eligibility → Lyzr</p></div><div className="mini-stat"><b>{results.length || '—'}</b><span>matches ready</span></div></div></section>
    <main>
      <div className="tabs"><button className={tab==='discover'?'active':''} onClick={()=>setTab('discover')}>{t.discover}</button><button className={tab==='profile'?'active':''} onClick={()=>setTab('profile')}>{t.profile}</button><button className={tab==='assistant'?'active':''} onClick={()=>setTab('assistant')}>{t.assistant}</button></div>
      {error&&<div className="error">{error}</div>}
      {tab==='profile'&&<section className="panel"><div className="panel-title"><div><p className="eyebrow">PERSONALIZED DISCOVERY</p><h2>Your benefit profile</h2></div><span className="step">01 / 01</span></div><div className="form-grid"><label>{t.age}<input type="number" value={profile.age} onChange={e=>setProfile({...profile,age:+e.target.value})}/></label><label>{t.state}<select value={profile.state} onChange={e=>setProfile({...profile,state:e.target.value})}><option>Tamil Nadu</option><option>Kerala</option><option>Karnataka</option><option>Andhra Pradesh</option><option>Telangana</option><option>Maharashtra</option><option>Delhi</option><option>All India</option></select></label><label>{t.occupation}<select value={profile.occupation} onChange={e=>setProfile({...profile,occupation:e.target.value})}><option value="student">Student</option><option value="farmer">Farmer</option><option value="street_vendor">Street vendor</option><option value="entrepreneur">Entrepreneur</option><option value="retirement">Retired / planning retirement</option><option value="worker">Worker</option></select></label><label>{t.income}<input type="number" value={profile.annual_income??''} onChange={e=>setProfile({...profile,annual_income:e.target.value===''?null:+e.target.value})}/></label><label>Gender<select value={profile.gender} onChange={e=>setProfile({...profile,gender:e.target.value})}><option value="any">Prefer not to say</option><option value="female">Female</option><option value="male">Male</option></select></label><label>Family size<input type="number" min="1" value={profile.family_size} onChange={e=>setProfile({...profile,family_size:+e.target.value})}/></label></div><div className="events"><b>Life events</b><div>{events.map(e=><button key={e} className={profile.life_events.includes(e)?'chip selected':'chip'} onClick={()=>toggleEvent(e)}>{e}</button>)}</div></div><button className="primary wide" onClick={match}>{t.find} →</button></section>}
      {tab==='assistant'&&<section className="assistant panel"><div className="panel-title"><div><p className="eyebrow">LYZR AI + QDRANT</p><h2>Ask about benefits</h2></div><span className="status">● Online when configured</span></div><div className="suggestions">{['What can I get as a student?','Any health support for my family?','I am starting a small business.'].map(x=><button onClick={()=>setQuestion(x)} key={x}>{x}</button>)}</div><div className="ask-row"><input value={question} onChange={e=>setQuestion(e.target.value)} onKeyDown={e=>e.key==='Enter'&&ask()} placeholder="Ask a government-scheme question…"/><button className="primary" onClick={ask}>{loading?'…':t.ask}</button></div>{answer&&<div className="answer"><div className="answer-badge">{source}</div><p>{answer}</p></div>}</section>}
      {tab==='discover'&&<section className="results"><div className="section-head"><div><p className="eyebrow">PERSONALIZED RESULTS</p><h2>{results.length?'Recommended for you':'Start with your profile'}</h2></div>{results.length>0&&<button className="outline" onClick={()=>setTab('profile')}>Edit profile</button>}</div>{results.length===0?<div className="empty"><div className="empty-icon">✓</div><h3>Let BenefitBridge find your matches</h3><p>Build a profile once. The engine retrieves relevant schemes, checks your profile against the stored rules and explains why each result appeared.</p><button className="primary" onClick={()=>setTab('profile')}>Build my profile →</button></div>:<div className="cards">{results.map(s=><SchemeCard key={s.id} scheme={s}/>)}</div>}</section>}
    </main>
    <footer><span>BenefitBridge • Prototype for social impact</span><span>Always verify final eligibility on the official portal.</span></footer>
  </div>
}

function SchemeCard({scheme}){return <article className="scheme"><div className="scheme-top"><span className="category">{scheme.category}</span><span className="score">{scheme.score}% match</span></div><h3>{scheme.name}</h3><p>{scheme.short_description}</p><div className="benefit"><b>Benefit</b><span>{scheme.benefit}</span></div><div className="why"><b>Why it matched</b>{scheme.reasons.slice(0,3).map((r,i)=><span key={i}>✓ {r}</span>)}</div><div className="docs"><b>Documents</b><span>{scheme.documents.join(' • ')}</span></div><a className="apply" href={scheme.official_url} target="_blank" rel="noreferrer">Official portal ↗</a></article>}

createRoot(document.getElementById('root')).render(<App/>);
