import './Button.css';

export interface ButtonProps {
  type: 'primary' | 'secondary';
  label: string;
  styled: 'default' | 'highlight';
  onClick?: () => void;
}

function Button(props: ButtonProps) {
  const { type, label, styled, onClick } = props;

  return (
    <button data-type={type} onClick={onClick} className={styled}>
      {label}
    </button>
  );
}

export default Button;