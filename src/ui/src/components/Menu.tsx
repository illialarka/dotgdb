import classes from './Menu.module.css';

function Menu() {
  return (
    <div className={classes.container}>
      <div className={classes.item}>
        <a>File</a>
      </div>
      <div className={classes.item}>
        <a>View</a>
      </div>
      <div className={classes.item}>
        <a>Help</a>
      </div>
    </div>
  );
}

export default Menu;
