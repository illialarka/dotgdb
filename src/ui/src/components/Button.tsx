interface ButtonProps {
  label?: string;
  callback?: () => void;
  icon?: JSX.Element;
};

const Button = (props: ButtonProps) => {
  const { label, callback, icon } = props;

  return (
    <button
      type="button"
      onClick={callback}
      className="darker px-2 text-sm font-medium leading-4 border border-gray-600">
      {icon}
      {label}
    </button>
  );
};

export default Button;