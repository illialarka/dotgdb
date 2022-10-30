import './App.css';
import Button from './components/Button';
import Code from './components/Code';
import Link from './components/Link';

function App() {
  return (
    <div className="App">
      <Button type='primary' label='Button'></Button>
      <Link label='Link example' target='_blank'></Link>
      <Code></Code>
    </div>
  );
}

export default App;