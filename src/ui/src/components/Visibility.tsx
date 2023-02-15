import { Tab } from '@headlessui/react'
import { useAppSelector } from '../store/hooks';
import { selectLogs } from '../store/selectors';

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
}

const Visibility = () => {
  const logs = useAppSelector(selectLogs);

  return (
    <div className="flex flex-col text-white text-sm">
      <Tab.Group>
        <div className="bg-gray-600 p-1">
          Visibility
        </div>
        <Tab.List className="flex space-x-2 bg-gray-500">
          <Tab
            className={({ selected }) =>
              classNames(
                'font-medium leading-5 text-gray-100 p-1',
                'outline-none',
                selected
                  ? 'bg-gray-400 shadow'
                  : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
              )
            }>
            Logs
          </Tab>
        </Tab.List>
        <Tab.Panels className="flex ">
          <Tab.Panel className="overflow-auto flex flex-col max-h-min ">
            {logs.map((log, index) => (
              <span key={index}>{log}</span>
            ))}
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
};

export default Visibility;