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

const BreakpointView = (
  props: { breakpoint: Breakpoint }
) => {
  const { breakpoint } = props;
  return (
    <div className="flex flex-row items-center">
      <span>{breakpoint.id}</span>
    </div>
  );
};

const Sidebar = () => {
  const breakpoints = useAppSelector(selectBreakpoints);
  
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
              <div className="flex flex-col">
                {breakpoints.map((breakpoint, index) =>
                  <BreakpointView key={index} breakpoint={breakpoint}/>)}
              </div>
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
