import classes from './Link.module.css';

export interface LinkProps {
    target: "_blank" | "_self" | "_parent" | "_top"
    href?: string;
    label: string;
}

function Link(props: LinkProps) {
    const { target, href, label } = props;

    return <a className={classes.link} href={href} target={target}>{label}</a>
}

export default Link;