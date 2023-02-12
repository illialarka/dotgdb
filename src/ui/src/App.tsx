import './App.css';
import CodeView from './components/CodeView';
import Sidebar from './components/Sidebar';
import Toolbar from './components/Toolbar';
import Visibility from './components/Visibility';

function App() {
  return (
    <div className="layout">
      <div className="toolbar">
        <Toolbar></Toolbar>
      </div>
      <div className="codeview layout-element">
        <CodeView></CodeView>
      </div>
      <div className="visibility layout-element">
        <Visibility></Visibility>
      </div>
      <div className="sidebar layout-element">
        <Sidebar></Sidebar>
      </div>
    </div>
  );
}

export default App;
