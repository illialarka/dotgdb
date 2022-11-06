import classes from './Button.module.css';

export interface ButtonProps {
  type: 'primary' | 'secondary';
  disabled: boolean;
  label: string;
  styled: 'default' | 'highlight';
  onClick?: () => void;
}

function Button(props: ButtonProps) {
  const { type, label, styled, onClick, disabled } = props;

  return (
    <button
      data-type={type}
      onClick={onClick}
      className={`${classes.btn} ${styled === 'highlight' ? classes.highlight : classes.default}`}
      disabled={disabled}>
      {label}
    </button>
  );
}

export default Button;