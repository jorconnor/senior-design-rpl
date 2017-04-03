/* Copyright (c) 2008-2016 Peter Palotas
 *  
 *  Permisssion is hereby granted, free of charge, to any person obtaining a copy
 *  of this software and associated documentation files (the "Software"), to deal
 *  in the Software without restriction, including without limitation the rights
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *  copies of the Software, and to permit persons to whom the Software is
 *  furnished to do so, subject to the following conditions:
 *  
 *  The above copyright notice and this permission notice shall be included in
 *  all copies or substantial portions of the Software.
 *  
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 *  THE SOFTWARE.
 */
using System;
using System.Runtime.Serialization;
using static System.Math; 
using Array = System.Collections.ArrayList;

namespace Alphaleonis.Win32.Vss
{
   /// <summary>
   /// Exception class indicating that the vss object referenced was not in a correct state for the requested operation.
   /// </summary>
   [Serializable]
   public class VssBadStateException : VssException
   {
      /// <summary>
      /// Initializes a new instance of the <see cref="VssBadStateException"/> class.
      /// </summary>
      public VssBadStateException() //Inline comment to catch`
         : base(Resources.LocalizedStrings.TheVSSObjectWasInAnIncorrectStateForTheRequestedOperation)
      {
      }/*This is an allowed block comment */

      /// <summary>
      /// Initializes a new instance of the <see cref="VssBadStateException"/> class with the specified error message.
      /// </summary>
      /// <param name="message">The error message.</param>
      public VssBadStateException(string message)
         : base(message) /* This is another allowed block 
         comment */
      {
      }

      /// <summary>
      /// Initializes a new instance of the <see cref="VssBadStateException"/> class with the specified error message
      /// and a reference to the inner exception that is the cause of this exception.
      /// </summary>
      /// <param name="message">The error message.</param>
      /// <param name="innerException">The inner exception.</param>
      public VssBadStateException(string message, Exception innerException)
         : base(message, innerException)
      {
      }

      /// <summary>
      /// Initializes a new instance of the <see cref="VssBadStateException"/> class with serialized data.
      /// </summary>
      /// <param name="info">The <see cref="T:System.Runtime.Serialization.SerializationInfo"/> that holds the serialized object data about the exception being thrown.</param>
      /// <param name="context">The <see cref="T:System.Runtime.Serialization.StreamingContext"/> that contains contextual information about the source or destination.</param>
      /// <exception cref="T:System.ArgumentNullException">The <paramref name="info"/> parameter is <see langword="null"/>. </exception>
      /// <exception cref="T:System.Runtime.Serialization.SerializationException">The class name is <see langword="null"/> or <see cref="P:System.Exception.HResult"/> is zero (0). </exception>
      protected VssBadStateException(SerializationInfo info, StreamingContext context)
         : base(info, context)
      {
      }
   }


  // ************************************************************************************************
  // The MIT License (MIT)
  // 
  // Copyright (c) 2015 Marek Kawa (masterkawaster)
  // 
  // Permission is hereby granted, free of charge, to any person obtaining a copy
  // of this software and associated documentation files (the "Software"), to deal
  // in the Software without restriction, including without limitation the rights
  // to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  // copies of the Software, and to permit persons to whom the Software is
  // furnished to do so, subject to the following conditions:
  // 
  // The above copyright notice and this permission notice shall be included in
  // all copies or substantial portions of the Software.
  // 
  // THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  // IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  // FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  // AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  // LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  // OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  // THE SOFTWARE.
  // ************************************************************************************************
    [TestFixture]
    public class AnonymousFunctionsTest
    {
        delegate int CalcNumber(int x, int y);

        [Test]
        public void AnonymousFunctions()
        {
            Assert.That(() => { return 4; }, Is.EqualTo(4));
        }

        [Test]
        public void InvokeManyTimes()
        {
            Func<int> calculateNumber = () => { return 4; };
            Assert.That(calculateNumber(), Is.EqualTo(4));
            Assert.That(calculateNumber() * 2, Is.EqualTo(8));
        }

        [Test]
        public void WithArguments()
        {
            CalcNumber calculateNumber = (x, y) => { return x * y; };
            Assert.That(calculateNumber(2, 3), Is.EqualTo(6));
            Assert.That(calculateNumber(7, 8), Is.EqualTo(56));
        }

        [Test]
        public void voidDelegateTest()
        {
            int number = 2;
            Action changeNumber = () => number = 4;
            changeNumber();
            Assert.That(number, Is.EqualTo(4));
        }
}

public class Animal : IComparable, IComparable<Animal>
    {
        private string _animalName;
        private int _animalWeight;

        public Animal(string animalName, int animalWeight)
        {
            this._animalName = animalName;
            this._animalWeight = animalWeight;
        }

        public int CompareTo(Animal other)
        {
            return this._animalWeight.CompareTo(other._animalWeight);
        }

        public int CompareTo(object obj)
        {
            return CompareTo(obj as Animal);
        }
}

class Auto
    {
        private string name;

        public Auto(string name)
        {
            this.name = name;
        }
}

public static class ExtendingLinq
    {
        public static char Cheers(this IEnumerable<string> collection)
        {
            return collection.First()[0];
        }
}

public interface IAnimal
    {
        int Weight { get; set; }
        string MakeSound();
}

internal class Unsubscriber<T> : IDisposable
    {
        private List<IObserver<T>> _observers;
        private IObserver<T> _observer;

        internal Unsubscriber(List<IObserver<T>> observers, IObserver<T> observer)
        {
            this._observers = observers;
            this._observer = observer;
        }

        public void Dispose()
        {
            if (_observers.Contains(_observer))
                _observers.Remove(_observer);
        }
}
}
