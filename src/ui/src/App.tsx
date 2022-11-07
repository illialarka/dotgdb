import { useEffect, useState } from 'react';
import './App.css';
import Button from './components/Button';
import Link from './components/Link';
import Menu  from './components/Menu';
import { selectExecutable } from './reducers/ExecutableReducer';
import { useAppSelector } from './reducers/hooks';
import Load from './views/Load';

function App() {
  const [activeTab, setActiveTab] = useState('load');
  const [isExecutableSelected, setIsExecutableSelected] = useState(false);
  const executable = useAppSelector(selectExecutable);

  useEffect(() => {
    setIsExecutableSelected(!!executable.path && executable.path !== '');
  }, [ executable ]);

  const tabSelection = (tab: string) => {
    if (executable.path && executable.path.length > 0) {
      setActiveTab(tab);
    }
  }

  const tabContentClass = (tab: string) => {
    return activeTab === tab ? "active-tab" : "hidden-tab";
  }

  const tabButtonStyle = (tab: string) => {
    return activeTab === tab ? "highlight" : "default";
  }

  return (
    <div className="app">
        <div className="main-header">
          <Menu></Menu>
          <div className='text'>
            <Button type='primary' styled={tabButtonStyle('load')} label='Load' disabled={false} onClick={() => tabSelection('load')}/>
            <Button type='primary' styled={tabButtonStyle('environment')} disabled={!isExecutableSelected} label='Environment' onClick={() => tabSelection('environment')}/>
            <Button type='primary' styled={tabButtonStyle('script')} disabled={!isExecutableSelected} label='Script' onClick={() => tabSelection('script')}/>
            <Button type='primary' styled={tabButtonStyle('debug-output')} disabled={!isExecutableSelected} label='Debug Output' onClick={() => tabSelection('debug-output')}/>
          </div>
        </div>

      <div className="main">
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
          <div className={tabContentClass('debug-output')}>
            Debug Output
          </div>
 
        </div>

        <div className="tools">
          Side tools
          <Button disabled={false} type='primary' styled='default' label='Button'></Button>
          <Link label='Link example' target='_blank'></Link>
          <div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
