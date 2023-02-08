import React from "react";

class Loader extends React.Component {
  render() {
    return (
      <div className="overflow-hidden bg-white shadow sm:rounded-lg m-5">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900">Select Executable</h3>
        </div>
        <div className="border-t border-gray-200">
          <div className="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Executable file 
              <p className="mt-1 max-w-2xl text-xs text-gray-500">
                Select an executable binary file (.dll, .exe), .NET applicaiton.
              </p>
            </dt>
            <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
              <button type="button" className="ml-5 rounded-md border border-gray-300 bg-white py-2 px-3 text-sm font-medium leading-4 text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                Select file 
              </button>
            </dd>
          </div>
          <div className="border-t px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Source code file 
              <p className="mt-1 max-w-2xl text-xs text-gray-500">
                Select a source code file (*.cs) to place breakpoint. 
              </p>
            </dt>
            <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
              <button type="button" className="ml-5 rounded-md border border-gray-300 bg-white py-2 px-3 text-sm font-medium leading-4 text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                Select file 
              </button>
            </dd>
          </div>
        </div>
      </div>
    );
  }
}

export default Loader;