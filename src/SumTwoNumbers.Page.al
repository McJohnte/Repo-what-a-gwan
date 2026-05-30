page 50100 "Sum Two Numbers"
{
    Caption = 'Sum Two Numbers';
    PageType = StandardDialog;
    ApplicationArea = All;
    UsageCategory = Tasks;

    layout
    {
        area(Content)
        {
            group(Input)
            {
                Caption = 'Input';

                field(FirstNumber; FirstNumber)
                {
                    ApplicationArea = All;
                    Caption = 'First Number';
                    ToolTip = 'Specifies the first number to add.';

                    trigger OnValidate()
                    begin
                        CalculateSum();
                    end;
                }
                field(SecondNumber; SecondNumber)
                {
                    ApplicationArea = All;
                    Caption = 'Second Number';
                    ToolTip = 'Specifies the second number to add.';

                    trigger OnValidate()
                    begin
                        CalculateSum();
                    end;
                }
            }
            group(Output)
            {
                Caption = 'Result';

                field(Sum; Sum)
                {
                    ApplicationArea = All;
                    Caption = 'Sum';
                    Editable = false;
                    ToolTip = 'Specifies the sum of the two numbers.';
                }
            }
        }
    }

    var
        FirstNumber: Decimal;
        SecondNumber: Decimal;
        Sum: Decimal;

    local procedure CalculateSum()
    var
        SumTwoNumbers: Codeunit "Sum Two Numbers";
    begin
        Sum := SumTwoNumbers.Add(FirstNumber, SecondNumber);
    end;
}
