codeunit 50100 "Sum Two Numbers"
{
    /// <summary>
    /// Returns the sum of two decimal numbers.
    /// </summary>
    /// <param name="FirstNumber">The first addend.</param>
    /// <param name="SecondNumber">The second addend.</param>
    /// <returns>The sum of FirstNumber and SecondNumber.</returns>
    procedure Add(FirstNumber: Decimal; SecondNumber: Decimal): Decimal
    begin
        exit(FirstNumber + SecondNumber);
    end;
}
