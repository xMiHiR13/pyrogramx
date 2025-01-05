#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Callable

import pyrogram

from .handler import Handler


class ErrorHandler(Handler):
    """The Error handler class. Used to handle errors.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_error` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new edited message arrives. It takes *(client, message)*
            as positional arguments (look at the section below for a detailed description).

        errors (``Exception`` | List of ``Exception``):
            Pass one or exception classes to allow only a subset of errors to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        update (:obj:`~pyrogram.types.Update`):
            The received update that caused the error.

        error (``Exception``):
            The error that was raised.
    """

    def __init__(self, callback: Callable, errors=None):
        if errors is None:
            errors = [Exception]
        elif not isinstance(errors, list):
            errors = [errors]

        self.errors = errors
        super().__init__(callback)

    async def check(
        self,
        client: "pyrogram.Client",
        update: pyrogram.types.Update,
        error: Exception
    ) -> bool:
        if isinstance(error, self.errors):
            await self.callback(client, update, error)
            return True
        return False
