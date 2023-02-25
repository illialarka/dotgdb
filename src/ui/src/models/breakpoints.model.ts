export class Breakpoint {
    id: string;
    kind: string;
    source: string;
    method: string;
    line_number: number;

    constructor(id: string, kind: string, source: string, method: string, line_number: number) {
        this.id = id;
        this.kind = kind;
        this.source = source;
        this.method = method;
        this.line_number = line_number
    }
}