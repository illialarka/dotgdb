import { Disclosure } from "@headlessui/react";
import { Breakpoint } from "../models/breakpoints.model";
import { useAppSelector } from "../store/hooks";
import { selectBreakpoints } from "../store/selectors";

const Chevron = () => {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
    </svg>
  );
};

const BreakpointsTable = () => {
  const breakpoints = useAppSelector(selectBreakpoints);

  return (
    <table className="table-auto w-full cursor-default">
      <thead className="border-b border-gray-400 text-left">
        <tr className="text-gray-400 text-xs">
          <th></th>
          <th>#</th>
          <th>Method</th>
          <th>File</th>
          <th>Line</th>
        </tr>
      </thead>
      <tbody>
        {breakpoints.map((breakpoint: Breakpoint, index: number) =>
          <tr key={index} className="border-b border-gray-500 py-2">
            <td className="text-red-500">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
                <path fillRule="evenodd" d="M2 10a8 8 0 1116 0 8 8 0 01-16 0zm5-2.25A.75.75 0 017.75 7h4.5a.75.75 0 01.75.75v4.5a.75.75 0 01-.75.75h-4.5a.75.75 0 01-.75-.75v-4.5z" clipRule="evenodd" />
              </svg>
            </td>
            <td>{breakpoint.id}</td>
            <td>{breakpoint.method}</td>
            <td className="truncate cursor-pointer">{breakpoint.source}</td>
            <td>{breakpoint.line_number}</td>
          </tr>
        )}
      </tbody>
    </table>
  );
};

const Sidebar = () => {

  return (
    <div className="flex flex-col text-white text-sm">
      <div className="bg-gray-600 p-1">
        Sidebar
      </div>
      <Disclosure>
        {({ open }) => (
          <>
            <Disclosure.Button className="flex flex-row p-1 justify-between text-white bg-gray-500 border-t">
              <span>Breakpoints</span>
              <div className={`${open ? 'rotate-180 transform' : ''
                } h-5 w-5 text-white`}>
                <Chevron />
              </div>
            </Disclosure.Button>
            <Disclosure.Panel>
              <BreakpointsTable />
            </Disclosure.Panel>
          </>
        )}
      </Disclosure>
      <Disclosure>
        {({ open }) => (
          <>
            <Disclosure.Button className="flex flex-row p-1 justify-between text-white bg-gray-500 border-t">
              <span>Locals</span>
              <div className={`${open ? 'rotate-180 transform' : ''
                } h-5 w-5 text-white`}>
                <Chevron />
              </div>
            </Disclosure.Button>
            <Disclosure.Panel>
              Locals appear there.
            </Disclosure.Panel>
          </>
        )}
      </Disclosure>
      <Disclosure>
        {({ open }) => (
          <>
            <Disclosure.Button className="flex flex-row p-1 justify-between text-white bg-gray-500 border-t">
              <span>Method parameters</span>
              <div className={`${open ? 'rotate-180 transform' : ''
                } h-5 w-5 text-white`}>
                <Chevron />
              </div>
            </Disclosure.Button>
            <Disclosure.Panel>
              Methor params appear there.
            </Disclosure.Panel>
          </>
        )}
      </Disclosure>
    </div>
  );
};

export default Sidebar;
