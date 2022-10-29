import './Button.css';

export interface ButtonProps {
  type: 'primary' | 'secondary';
  label: string;
}

function Button(props: ButtonProps) {
  const { type, label } = props;

  return (
    <button data-type={type}>
      {label}
    </button>
  );
}

export default Button;