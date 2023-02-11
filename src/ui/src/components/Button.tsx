interface ButtonProps {
  label: string;
  callback?: () => void;
}; 

const Button = (props: ButtonProps) => {
  const { label, callback } = props;

  return (
    <button
      type="button"
      onClick={callback}
      className="rounded-sm border border-gray-300 bg-white py-1 px-2 text-xs font-medium leading-4 text-gray-700 shadow-inner hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-gray-500 focus:ring-offset-1">
      {label}
    </button>
  );
};

export default Button;