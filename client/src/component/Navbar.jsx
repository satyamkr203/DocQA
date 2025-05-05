import FileUpload from './FileUpload';

const Navbar = ({ onFileUpload, documentName, isLoading }) => {
  return (
    <nav className="flex items-center justify-between p-4 bg-white shadow-md">
      <div className="flex items-center">
        <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center mr-3">
          <span className="text-white font-bold">DQ</span>
        </div>
        <h1 className="text-xl font-bold text-gray-800">DocQA</h1>
      </div>
      
      <div className="flex items-center gap-4">
        {documentName && (
          <span className="text-sm text-gray-600 hidden md:inline">
            Active: {documentName}
          </span>
        )}
        <FileUpload 
          onFileUpload={onFileUpload} 
          isLoading={isLoading} 
        />
      </div>
    </nav>
  );
};

export default Navbar;