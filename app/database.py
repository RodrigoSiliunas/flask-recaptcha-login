from pymongo import MongoClient

"""
==========================================================================
 ➠ Database Configuration File (https://github.com/RodrigoSiliunas/)
 ➠ Section By: Rodrigo Siliunas (Rô: https://github.com/RodrigoSiliunas)
 ➠ Related system: Database (PyMongo)
 ➠ Tips: To avoid circular imports this file is required. Please don't delete this file.
==========================================================================
"""

client = MongoClient('mongodb://localhost:27017/')
