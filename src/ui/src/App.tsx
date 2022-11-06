import { useState } from 'react';
import './App.css';
import Button from './components/Button';
import Code from './components/Code';
import FileInput from './components/FileInput';
import Link from './components/Link';
import Menu  from './components/Menu';
import Load from './views/Load';

const tabs = ["load", "environment", "script"]

function App() {
  const [activeTab, setActiveTab] = useState('load');

  const tabContentClass = (tab: string) => {
    return activeTab === tab ? "active-tab" : "hidden-tab";
  }

  const tabButtonStyle = (tab: string) => {
    return activeTab === tab ? "highlight" : "default";
  }

  return (
    <div className="app">
      <div className="main">
        <div className="main-header">
          <Menu></Menu>
          <div className='text'>
            <Button type='primary' styled={tabButtonStyle('load')} label='Load' onClick={() => setActiveTab('load')}></Button>
            <Button type='primary' styled={tabButtonStyle('environment')} label='Environment' onClick={() => setActiveTab('environment')}></Button>
            <Button type='primary' styled={tabButtonStyle('script')} label='Script' onClick={() => setActiveTab('script')}></Button>
          </div>
        </div>
        <div className='main-view text'>
          <div className={tabContentClass('load')}>
            <Load ></Load>
          </div>
          <div className={tabContentClass('environment')}>
            Env Tab
          </div>
          <div className={tabContentClass('script')}>
            Script Tab here
          </div>
        </div>
      </div>
      <div className="tools">
        Side tools
        <Button type='primary' styled='default' label='Button'></Button>
        <Link label='Link example' target='_blank'></Link>
        <div>
        </div>
      </div>
    </div>
  );
}

export default App;