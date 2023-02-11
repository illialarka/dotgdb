import './App.css';
import CodeView from './components/CodeView';
import Toolbar from './components/Toolbar';
import Visibility from './components/Visibility';

function App() {
  return (
    <div className="layout">
      <div className="toolbar">
        <Toolbar></Toolbar>
      </div>
      <div className="codeview border m-2">
        <CodeView></CodeView>
      </div>
      <div className="visibility border m-2">
        <Visibility></Visibility>
      </div>
      <div className="sidebar border m-2">
        Sidebar
      </div>
    </div>
  );
}

export default App;
