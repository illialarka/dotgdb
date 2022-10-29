import './Button.css';

export interface ButtonProps {
  type: 'primary' | 'secondary';
  label: string;
  onClick?: () => void;
}

function Button(props: ButtonProps) {
  const { type, label, onClick } = props;

  return (
    <button data-type={type} onClick={onClick}>
      {label}
    </button>
  );
}

export default Button;