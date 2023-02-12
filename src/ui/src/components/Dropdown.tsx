import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
};

interface DropdownProps {
  label: string;
  items: DropdownItem[];
};

interface DropdownItem {
  label: string;
  callback: () => void;
};

const Dropdown = (props: DropdownProps) => {
  const { label, items } = props;

  return (
    <Menu as="div" className="relative inline-block text-left">
      <div>
        <Menu.Button className="hover:bg-gray-700 px-2 py-1">
          {label}
        </Menu.Button>
      </div>
      <Transition
        as={Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items className="absolute left-0 z-10 mt-2 w-56 origin-top-right bg-gray-700 shadow-lg focus:outline-none">
          <div className="py-1">
            {items.map(item => 
                  <Menu.Item>
                    {({ active }) => (
                      <button
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-white',
                          'block px-4 py-2 text-sm w-full text-left'
                        )}
                        onClick={item.callback}
                      >
                        {item.label}
                      </button>
                    )}
                  </Menu.Item>)
            }
          </div>
        </Menu.Items>
      </Transition>
    </Menu>
  )
}

export default Dropdown;