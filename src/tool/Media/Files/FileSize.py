from App.Objects.Object import Object

class FileSize(Object):
    @staticmethod
    def convert_from(input_val: int | float, input_unit: str, output_unit: str, use_decimal: bool = False, round_rate: int = 2) -> int:
        base = 1000 if use_decimal else 1024
        units = {'b': 0}
        i = 1
        for item in ['kb', 'mb', 'gb', 'tb', 'pb']:
            units[item] = i
            i += 1

        # If not bytes, converting to them
        if input_unit != 'b':
            input_val = input_val * (base ** units[input_unit])

        val = input_val / (base**units[output_unit])
        if round_rate is not None:
            val = round(val, round_rate)

        if round_rate == 0:
            val = int(val)

        return val
