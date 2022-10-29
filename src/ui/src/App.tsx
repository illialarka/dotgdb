import './App.css';
import Button from './components/Button';
import Link from './components/Link';

function App() {
  return (
    <div className="App">
      <Button type='primary' label='Button'></Button>
      <Link label='Link example' target='_blank'></Link>
    </div>
  );
}

export default App;