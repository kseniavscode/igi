import React from 'react';
import ReactDOM from 'react-dom';

function App() {
  return (
    <div style={{textAlign: 'center', marginTop: '50px'}}>
      <h1>🚀 MERN Stack в Docker работает!</h1>
      <p>React + Node + Mongo</p>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
