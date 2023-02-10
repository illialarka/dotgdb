import React from "react";

class Toolbar extends React.Component {
  render() {
    return (
      <div className="grid grid-cols-3 gap-3 p-3">
        <div className="flex flex-wrap items-stretch w-full p-2 relative">
          <input type="text" className="block w-full rounded-md border-gray-300 pl-7 pr-12 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm flex-shrink flex-grow leading-normal flex-1 border h-10 rounded-r-none px-3 relative" placeholder="Select executable file"/>
          <div className="flex -mr-px">
            <span className="flex items-center leading-normal bg-grey-lighter rounded rounded-l-none border border-l-0 border-grey-light px-3 whitespace-no-wrap text-grey-dark text-sm">Select</span>
          </div>	
        </div>	
        <div className="...">02</div>
        <div className="...">03</div>
      </div>
    )
    return (
      <div className="gird gird-cols-3 gap-3 overflow-hidden border-b p-3">
        <div className="col-span-1 flex flex-row space-x-2 items-center border-r pr-2 max-w-md">
        </div>
        <div className="col-span-2 flex flex-row space-x-2 items-center border-r pr-2 max-w-md">
          <span className="truncate">/Users/illialarka/projects/dotgdb/src/ui/src /Users/illialarka/projects/dotgdb/src/ui/src</span>
          <label htmlFor="file-upload" className="relative cursor-pointer rounded-md bg-white font-medium text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 hover:text-indigo-500">
            <button type="button" className="rounded-md border border-gray-300 bg-white py-2 px-3 text-sm font-medium leading-4 text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Select</button>
          </label>
        </div>
        <div>Run/Step in/Step over</div>
      </div>
    );
  }
}

export default Toolbar;