import { Disclosure } from "@headlessui/react";
import { Breakpoint } from "../models/breakpoints.model";
import { useAppSelector } from "../store/hooks";
import { selectBreakpoints } from "../store/selectors";
import './Sidebar.css';

const Chevron = () => {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
    </svg>
  );
};

const BreakpointsTable = () => {
  const breakpoints = useAppSelector(selectBreakpoints);

  const table = (
    <table className="table-auto min-w-full">
      <thead className="bg-gray-700 text-white">
        <tr className="text-xs">
          <th className="icon-column"></th>
          <th className="id-column text-left py-2">#</th>
          <th className="method-column text-left py-2">Method</th>
          <th className="source-column text-left py-2">Source</th>
          <th className="line-column text-left py-2">Line</th>
        </tr>
      </thead>
      <tbody className="text-gray-200">
        {breakpoints.map((breakpoint, index) =>
          <tr key={index} className="border-b border-gray-600">
            <td></td>
            <td className="text-left py-2">{breakpoint.id}</td>
            <td className="text-left py-2">{breakpoint.method}</td>
            <td className="text-left break-words py-2">{breakpoint.source}</td>
            <td className="text-left py-2">{breakpoint.line_number}</td>
          </tr>
        )}
      </tbody>
    </table>);

  const placeholder = (
    <div className="flex text-sm items-center">
      <span>There is no brekpoints.</span>
    </div>);

  return breakpoints?.length > 0
    ? table
    : placeholder;
};

const Sidebar = () => {

  return (
    <div className="flex flex-col text-white text-sm overflow-hidden">
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
    </div>
  );
};

export default Sidebar;
